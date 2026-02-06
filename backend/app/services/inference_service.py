import torch
import numpy as np
import io
from PIL import Image
from fastapi import UploadFile
from app.models.lung_model import load_model, predict
from app.utils.image_utils import preprocess_image
from app.utils.gradcam import generate_heatmap_image
from app.config import Settings

# --------------------------------------------------
# Device configuration
# --------------------------------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --------------------------------------------------
# Load model ONCE at startup
# --------------------------------------------------
try:
    settings = Settings()
    model = load_model(settings.model_path)
    model.to(DEVICE)
    model.eval()
    print(f"✅ Model loaded successfully on device: {DEVICE}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    raise

# --------------------------------------------------
# Inference function with heatmap generation
# --------------------------------------------------
async def run_inference(file: UploadFile, generate_heatmap: bool = True) -> dict:
    """
    Reads an uploaded image, preprocesses it, runs the model,
    generates heatmap, and returns comprehensive results.
    
    Returns:
        dict with:
            - prediction: str (normal/benign/malignant)
            - confidence: float (0-1)
            - probability_score: float (0-100)
            - probabilities: dict with all class probabilities
            - heatmap_image: str (base64 encoded) if generate_heatmap=True
    """
    # 1️⃣ Read image bytes
    image_bytes = await file.read()

    # 2️⃣ Get original image for heatmap (before preprocessing)
    original_image = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))

    # 3️⃣ Preprocess image → tensor
    tensor = preprocess_image(image_bytes)
    tensor = tensor.to(DEVICE)

    # 4️⃣ Run inference
    logits, prediction_dict = predict(model, tensor)
    
    # 5️⃣ Generate heatmap if requested
    heatmap_image = None
    if generate_heatmap:
        try:
            # Convert original image to RGB array if needed
            if len(original_image.shape) == 2:
                original_image = np.stack([original_image] * 3, axis=-1)
            elif original_image.shape[2] == 4:
                original_image = original_image[:, :, :3]
            
            heatmap_image, _ = generate_heatmap_image(
                model, tensor, original_image, 
                class_idx=prediction_dict['predicted_idx']
            )
        except Exception as e:
            print(f"Warning: Could not generate heatmap: {e}")
            heatmap_image = None

    # 6️⃣ Build response
    result = {
        "prediction": prediction_dict['prediction'],
        "confidence": prediction_dict['confidence'],
        "probability_score": prediction_dict['probability_score'],
        "probabilities": prediction_dict['probabilities'],
        "message": "lung-cancer-detection-v1"
    }
    
    if heatmap_image:
        result["heatmap_image"] = heatmap_image
    
    return result
