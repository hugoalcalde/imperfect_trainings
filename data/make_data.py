import torch
from torch.utils.data import Dataset, DataLoader, TensorDataset
from torchvision import transforms
import os
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

def make_data(folder='data/raw/'):

    targets_dir = folder + 'labels.csv'
    images_dir= folder + 'head_ct/'

    images = []
    size = (256, 256)

    files = os.listdir(images_dir)

    for i in files:
     # Open the image in black and white
        image = Image.open(images_dir + i).convert('L')
    
        # Resize the image to the common size
        image = image.resize(size, Image.BICUBIC)

        # Define a transformation to convert the image to a tensor
        transform = transforms.Compose([transforms.ToTensor()])  # Converts the image to a PyTorch tensor

        #  Apply the transformation to the image
        tensor_image = transform(image)
        images.append(tensor_image)

    images = torch.cat(images, dim=0)

    # Load the targets CSV file using pandas
    data_frame = pd.read_csv(targets_dir)

    # Extract the values from the DataFrame
    targets_values= data_frame.values[:,1] 

    # Convert the values to a PyTorch tensor
    targets = torch.tensor(targets_values, dtype=torch.float32)

    # Create a PyTorch dataset
    dataset = TensorDataset(images, targets)

    # Create a PyTorch data loader
    batch_size = 32
    data_loader = DataLoader(dataset, batch_size, shuffle=True)  

    torch.save(data_loader , 'data/processed.pt')

    return data_loader

