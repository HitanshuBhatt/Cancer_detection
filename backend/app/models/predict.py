import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
model = models.efficientnet_b0(weights=None)
num_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_features, 4)

model_path = r"C:\Users\Hitanshu\Documents\ai_lung\backend\app\models\savedmodels\lung_cancer_model.pth"
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

# Labels (match training)
labels = [
    "adenocarcinoma",
    "large.cell.carcinoma",
    "normal",
    "squamous.cell.carcinoma"
]

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

# Load image
image_path = r"C:\Users\Hitanshu\Documents\ai_lung\Datasets\validation\squamous.cell.carcinoma\000108 (3).png"  # replace with your test image path
image = Image.open(image_path).convert("RGB")
image = transform(image).unsqueeze(0).to(device)

# Prediction
with torch.no_grad():
    outputs = model(image)
    probabilities = torch.softmax(outputs, dim=1)
    predicted_idx = torch.argmax(probabilities, dim=1).item()

prediction = labels[predicted_idx]
confidence = probabilities[0][predicted_idx].item() * 100

print(f"Prediction: {prediction}")
print(f"Confidence: {confidence:.2f}%")