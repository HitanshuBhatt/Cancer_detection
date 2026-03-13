import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image

# Load model
model = models.efficientnet_b0(weights=None)

num_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_features, 4)

model.load_state_dict(torch.load("lung_model.pth"))

model.eval()

# Labels
labels = [
    "normal",
    "adenocarcinoma",
    "large.cell.carcinoma",
    "squamous.cell.carcinoma"
]

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

# Load image
image = Image.open("test_image.jpg").convert("RGB")

image = transform(image).unsqueeze(0)

# Prediction
with torch.no_grad():

    outputs = model(image)

    probabilities = torch.softmax(outputs, dim=1)

    predicted = torch.argmax(probabilities, dim=1)

prediction = labels[predicted.item()]
confidence = probabilities[0][predicted.item()].item() * 100

print("Prediction:", prediction)
print("Confidence:", confidence)