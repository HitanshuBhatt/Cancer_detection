# """
# Grad-CAM implementation for generating heatmaps showing where the model
# focuses its attention when detecting lung cancer.
# """
import torch
import torch.nn.functional as F
import numpy as np
import cv2
from typing import Tuple
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from io import BytesIO
import base64


class GradCAM:
    # """
    # Gradient-weighted Class Activation Mapping (Grad-CAM) for visualizing
    # model attention on lung CT scans.
    # """
    
    def __init__(self, model, target_layer):
        """
        Initialize Grad-CAM.
        
        Args:
            model: The PyTorch model
            target_layer: The convolutional layer to generate heatmaps from
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_full_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        """Save the activation maps."""
        self.activations = output
    
    def save_gradient(self, module, grad_input, grad_output):
        """Save the gradients."""
        self.gradients = grad_output[0]
    
    def generate_heatmap(self, input_tensor, class_idx=None):
        """
        Generate a heatmap for the given input.
        
        Args:
            input_tensor: Preprocessed input image tensor
            class_idx: Class index to generate heatmap for (None = use predicted class)
        
        Returns:
            Heatmap as numpy array
        """
        self.model.eval()
        input_tensor.requires_grad_()
        
        # Forward pass
        output = self.model(input_tensor)
        
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()
        
        # Backward pass
        self.model.zero_grad()
        output[0, class_idx].backward(retain_graph=True)
        
        # Get gradients and activations
        if self.gradients is None or self.activations is None:
            raise ValueError("Gradients or activations not captured. Check hook registration.")
        
        gradients = self.gradients[0].cpu().data.numpy()
        activations = self.activations[0].cpu().data.numpy()
        
        # Calculate weights (global average pooling of gradients)
        if len(gradients.shape) == 3:
            weights = np.mean(gradients, axis=(1, 2))
        else:
            weights = np.mean(gradients, axis=(0, 1))
        
        # Generate heatmap
        if len(activations.shape) == 3:
            heatmap = np.zeros(activations.shape[1:], dtype=np.float32)
            for i, w in enumerate(weights):
                if i < activations.shape[0]:
                    heatmap += w * activations[i, :, :]
        else:
            heatmap = np.zeros(activations.shape, dtype=np.float32)
            heatmap = activations * weights[0] if len(weights) > 0 else activations
        
        # Apply ReLU to only show positive contributions
        heatmap = np.maximum(heatmap, 0)
        
        # Normalize
        if np.max(heatmap) > 0:
            heatmap = heatmap / (np.max(heatmap) + 1e-8)
        
        return heatmap, class_idx
    
    def overlay_heatmap(self, original_image, heatmap, alpha=0.4):
        """
        Overlay heatmap on original image.
        
        Args:
            original_image: Original image as numpy array (H, W, 3)
            heatmap: Heatmap as numpy array (H, W)
            alpha: Transparency factor for heatmap overlay
        
        Returns:
            Overlaid image as numpy array
        """
        # Resize heatmap to match original image size
        heatmap_resized = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
        
        # Apply colormap
        heatmap_colored = cm.jet(heatmap_resized)[:, :, :3]
        heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
        
        # Overlay
        overlaid = cv2.addWeighted(original_image, 1 - alpha, heatmap_colored, alpha, 0)
        
        return overlaid


def get_target_layer(model):
    """
    Get the target layer for Grad-CAM from EfficientNet.
    """
    # For EfficientNet-B0 from torchvision, the structure is:
    # model.features -> Sequential containing blocks
    # We want the last convolutional block
    if hasattr(model, 'features'):
        # EfficientNet structure from torchvision
        features = model.features
        # Find the last Conv2d layer in the features
        last_conv = None
        for module in features.modules():
            if isinstance(module, torch.nn.Conv2d):
                last_conv = module
        if last_conv is not None:
            return last_conv
        # Fallback: use the last block
        if len(features) > 0:
            return features[-1]
    elif hasattr(model, 'blocks'):
        # Alternative EfficientNet structure
        return model.blocks[-1]
    
    # Fallback: find last conv layer in entire model
    last_conv = None
    for module in model.modules():
        if isinstance(module, torch.nn.Conv2d):
            last_conv = module
    if last_conv is not None:
        return last_conv
    
    raise ValueError("Could not find suitable target layer for Grad-CAM")


def generate_heatmap_image(model, input_tensor, original_image_array, class_idx=None):
    """
    Generate a complete heatmap visualization.
    
    Args:
        model: PyTorch model
        input_tensor: Preprocessed input tensor
        original_image_array: Original image as numpy array (H, W, 3)
        class_idx: Class index (None = use predicted class)
    
    Returns:
        Base64 encoded image string
    """
    # Ensure model is in eval mode but allows gradients
    model.eval()
    
    # Get target layer
    target_layer = get_target_layer(model)
    
    # Initialize Grad-CAM
    gradcam = GradCAM(model, target_layer)
    
    # Generate heatmap
    try:
        heatmap, predicted_class = gradcam.generate_heatmap(input_tensor, class_idx)
    except Exception as e:
        print(f"Error generating heatmap: {e}")
        # Return a simple visualization if heatmap generation fails
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.imshow(original_image_array)
        ax.set_title('Original CT Scan (Heatmap unavailable)', fontsize=12)
        ax.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_base64, class_idx if class_idx is not None else 0
    
    # Overlay on original image
    overlaid = gradcam.overlay_heatmap(original_image_array, heatmap)
    
    # Create visualization with side-by-side comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original image
    axes[0].imshow(original_image_array)
    axes[0].set_title('Original CT Scan', fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    # Heatmap only
    im = axes[1].imshow(heatmap, cmap='jet', interpolation='bilinear')
    axes[1].set_title('Attention Heatmap', fontsize=12, fontweight='bold')
    axes[1].axis('off')
    plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
    
    # Overlaid image
    axes[2].imshow(overlaid)
    axes[2].set_title('Overlay Visualization', fontsize=12, fontweight='bold')
    axes[2].axis('off')
    
    plt.tight_layout()
    
    # Convert to base64
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_base64, predicted_class
