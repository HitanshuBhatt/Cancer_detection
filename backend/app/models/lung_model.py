import torch 
import os 

import torch.nn as nn
import torch.optim as optim


from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader


#  re sizing images to 224*224
transform = transforms.Compose([
    transforms.Resize((224,224)), # resize image to 224*224
    transforms.ToTensor() # convert images to numbers using tensor 

])

#  loding the data 
train_dataset= datasets.ImageFolder( #training data
    "Datasets/train",
    transform=transform
)

validation_dataset= datasets.ImageFolder( #validation data
    "Datasets/validation",
    transform=transform
)

#  creating a dataloader this feeds the data in batches 
train_loader=DataLoader(
    train_dataset,
    batch_size=16, # number of batches in a single iteeration
    shuffle=True
)
validation_loader=DataLoader(
    validation_dataset,
    batch_size=16
)

#  loading the pre trained model with default weigths
model=models.efficientnet_b0(weights="DEFAULT")

#  changing the last layer to fit our data

num_features=model.classifier[1].in_features # number of features in the last layer 
model.classifier[1]= nn.Linear(num_features,4) # changing the last layer to fit the data which is 4 classes 

# moving the model to gpu if avialable 
device = torch.device("cuda" if torch.cuda.is_available()else"cpu")
model.to(device)

#  defining the loss function 
criterion= nn.CrossEntropyLoss()

#  defining the optimizer 
optimizer= optim.Adam(model.parameters(),lr=0.001) #learning rate as been set to 0.001 because as a pre trained model is
# being used so can nnot change weights too much

#  training the model 
#  trainig loop
num_epochs=10 # epochs is the number of times the model will see the entire dataset 
for epoch in range(num_epochs):
    model.train()  # setting the model to trainig mode
    running_loss=0.0
    for images, labels in train_loader:
        images=images.to(device) #this moves images to GPU
        labels=labels.to(device)  # moving labels to GPU 
        optimizer.zero_grad() # this clears the gradients fromthe previous iteration 
        outputs=model(images) 
        loss=criterion(outputs,labels)

        loss.backward() #this computes the gradients of the loss with respact to the model parameters
        optimizer.step() #this update the model [arameters bsased on the computed gradients]
        running_loss+= loss.item()
    print("Epoch", epoch+1, "loss:-", running_loss) #this prints the loss after each epoch

# saving the model 

# saving the model

save_dir = r"C:\Users\Hitanshu\Documents\ai_lung\backend\app\models\savedmodels"

# create folder if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

save_file = "lung_cancer_model.pth"
full_path = os.path.join(save_dir, save_file)

torch.save(model.state_dict(), full_path)

print(f"Model successfully saved to: {full_path}")


#  loading the model for prediction 
model.load_state_dict(torch.load(full_path, map_location=device)) # this loads the model weights from the file 

#  testing the model
model.eval() # sets model in evaluation mode

# prediction loop 
def predict(image_tensor):
    model.eval()
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        predicted = torch.argmax(probabilities, dim=1)
        return predicted, probabilities

#  convering prediction to labels
#   define labels 
labels = ["adenocarcinoma", 
          "large.cell.carcinoma",
          "normal",
          "squamous.cell.carcinoma"]
