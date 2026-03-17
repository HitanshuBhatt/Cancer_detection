import torch
from torchvision import models
import torch.nn as nn

MODEL_PATH = "models/lung_cancer_model.pth"

def load_model():

    model = models.efficientnet_b0(weights=None)

    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, 4)

    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))

    model.eval()

    return model