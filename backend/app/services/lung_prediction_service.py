from PIL import Image
import torch
from torchvision import transforms
from app.ml.model_loader import load_model

# Load model once
model = load_model()

labels = [
    "normal",
    "adenocarcinoma",
    "large.cell.carcinoma",
    "squamous.cell.carcinoma"
]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


async def predict_lung_cancer(file):
    image = Image.open(file.file).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        predicted = torch.argmax(probabilities, dim=1)

    label = labels[predicted.item()]
    confidence = probabilities[0][predicted.item()].item() * 100

    return {
        "prediction": label,
        "confidence": confidence
    }