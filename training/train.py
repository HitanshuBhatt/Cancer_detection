import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

import os 

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

# Load datasets

#  creating dynamic path to dataset folder 
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
train_dir= os.path.join(project_root,"Datasets","train")
validation_dir=os.path.join(project_root,"Datasets","validation")
train_dataset = datasets.ImageFolder(train_dir, transform=transform)
val_dataset = datasets.ImageFolder(validation_dir, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
print(train_dataset.class_to_idx)
val_loader = DataLoader(val_dataset, batch_size=16)

# Load EfficientNet
model = models.efficientnet_b0(weights="DEFAULT")

num_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_features, 4)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
#  to check if using gpu or cpu for training
print("using device:", device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 10

for epoch in range(epochs):

    model.train()
    running_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs} Loss: {running_loss:.4f}")

# Save model

#  define the file name 
save_file="lung_cancer_model.pth"
# getting the project root directory 
project_root= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#  building the full path to the backend/models 
save_dir = os.path.join(project_root,"backend","models")
os.makedirs(save_dir, exist_ok=True)  # makes the folder if it is not present 
full_path= os.path.join(save_dir, save_file)

# saving the model 
torch.save(model.state_dict(),full_path)

print("Model training complete and saved.",full_path)