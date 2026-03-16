from fastapi import FastAPI, UploadFile, File
from PIL import Image
import torch
from torchvision import transforms, models
import torch.nn as nn

app = FastAPI()

# Load model
model = models.efficientnet_b0(weights=None)

num_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_features, 4)

model.load_state_dict(torch.load(r"backend\models\lung_cancer_model.pth", map_location="cpu"))

model.eval()

labels = [
    "normal",
    "adenocarcinoma",
    "large.cell.carcinoma",
    "squamous.cell.carcinoma"
]

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])


@app.get("/")
def home():
    return {"message": "Lung Cancer Detection API Running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image = Image.open(file.file).convert("RGB")

    image = transform(image).unsqueeze(0)

    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(outputs, dim=1)

        predicted = torch.argmax(probabilities, dim=1)

    prediction = labels[predicted.item()]
    confidence = probabilities[0][predicted.item()].item() * 100

    return {
        "prediction": prediction,
        "confidence": confidence
    }