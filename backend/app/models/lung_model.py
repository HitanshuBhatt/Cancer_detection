import torch 
from torchvision import models  #importing model 
import torch.nn as nn
import torch.optim as optim


from torchvision import datasets, transforms, models
from torch.utils import dataloader


#  re sizing images to 224*224
transforms = transforms.compose([
    transforms.resize(224*224), # resize image to 224*224
    transforms.ToTensor() # convert images to numbers using tensor 

])

#  loding the data 
train_dataset= datasets.ImageFolder( #training data
    "Datasets/train",
    transform=transforms
)

validation_dataset= datasets.ImageFolder( #validation data
    "Datasets/validation",
    transform=transforms
)

#  creating a dataloader this feeds the data in batches 
train_loader=dataloader(
    train_dataset,
    batch_size=16, # number of batches in a single iteeration
    shuffle=True
)
validation_loader=dataloader(
    validation_dataset,
    batch_size=16
)

#  loading the pre trained model with default weigths
model=models.efficientnet_b0(weights="Default")

#  changing the last layer to fit our data

num_features=model.classifier[1].in_features # number of features in the last layer 
model.classifier[1]= nn.linear(num_features,3) # changing the last layer to fit the data which is 3 classes 

# moving the model to gpu if avialable 
device = torch.device("cuda" if torch.cuda.is_available()else"cpu")
model.to(device)

#  defining the loss function 

