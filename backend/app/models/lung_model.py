import torch
from torchvision import models
from typing import Literal, Tuple, Optional
from pydantic import BaseModel
import torch.nn as nn
import torch.nn.functional as F

# ---------------------------
# Pydantic model for API response
# ---------------------------
class InferenceResponse(BaseModel):
    prediction: Literal['normal', 'benign', 'malignant']
    confidence: float
    probability_score: float  # Percentage (0-100)
    message: str

# ---------------------------
# Enhanced EfficientNet-B0 model for lung cancer detection
# ---------------------------
def load_model(model_path: Optional[str] = None):
    """
    Loads EfficientNet-B0 with 3 output classes (normal, benign, malignant).
    Can load from checkpoint if provided.
    """
    # Load pretrained EfficientNet-B0 for better feature extraction
    model = models.efficientnet_b0(weights='DEFAULT')
    
    # Replace classifier for 3-class classification
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, 3)
    
    # Load weights if provided
    if model_path:
        try:
            checkpoint = torch.load(model_path, map_location='cpu')
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            else:
                model.load_state_dict(checkpoint)
            print(f"Loaded model weights from {model_path}")
        except Exception as e:
            print(f"Warning: Could not load model from {model_path}: {e}")
            print("Using pretrained EfficientNet-B0 with random classifier weights")
    
    model.eval()
    return model

# ---------------------------
# Predict function with detailed probabilities
# ---------------------------
def predict(model, tensor) -> Tuple[torch.Tensor, dict]:
    """
    Run inference on a preprocessed tensor.
    
    Returns:
        tuple: (logits, prediction_dict)
        prediction_dict contains:
            - predicted_idx: int
            - confidence: float (max probability)
            - probabilities: dict with all class probabilities
            - probability_score: float (percentage 0-100)
    """
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]
        predicted_idx = outputs.argmax(dim=1).item()
        confidence = probabilities[predicted_idx].item()
    
    labels = ['normal', 'benign', 'malignant']
    prediction_label = labels[predicted_idx]
    
    # Calculate probability score as percentage
    probability_score = confidence * 100.0
    
    # Get all class probabilities
    prob_dict = {
        label: float(prob.item()) * 100.0 
        for label, prob in zip(labels, probabilities)
    }
    
    prediction_dict = {
        'predicted_idx': predicted_idx,
        'prediction': prediction_label,
        'confidence': confidence,
        'probability_score': probability_score,
        'probabilities': prob_dict
    }
    
    return outputs, prediction_dict
