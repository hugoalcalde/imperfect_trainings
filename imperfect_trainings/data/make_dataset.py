import torch 
import os 
from torch.utils.data import TensorDataset, DataLoader, random_split
from torchvision import transforms
from torchvision.io import read_image, ImageReadMode
import pandas as pd 

if __name__ == '__main__':

    data_folder = "data/raw/head_ct/"
    data_files = os.listdir(data_folder)
    target_csv = pd.read_csv("data/raw/labels.csv")
    target_csv.columns = ["id", "hemorrhage"]

    # Creating empty lists to store the processed tensors : 

    images = []
    targets = []

    # Obtaining the tensors from the images : 

    transform_normalize = transforms.Normalize(mean = 1, std = 1)
    transform_resize = transforms.Resize(size=(90, 90), antialias = True)
    for image in data_files : 
        tensor_image = transform_resize(transform_normalize(read_image(data_folder + image, mode = ImageReadMode.GRAY ).type(torch.float32)))
        images.append(tensor_image)
        id = int(image.replace(".png", "").replace("00", ""))
        target = target_csv[target_csv["id"] == id]["hemorrhage"].item()
        targets.append(torch.tensor([target]))
    
    images, targets = torch.concatenate(images), torch.concatenate(targets)

    # Create a TensorDataset

    images = images.unsqueeze(1)
    dataset = TensorDataset(images, targets)

    # Creating the different sets for training, validation and testing 

    generator = torch.Generator().manual_seed(42)
    dataset_train, dataset_test = random_split(dataset, [0.75, 0.25], generator)
                 

    # Specify batch size for DataLoader

    batch_size = 32

    # Create a DataLoader for train set

    train_loader = DataLoader(dataset_train, batch_size=batch_size, shuffle=True)

    # Create DataLoader for test set 

    test_loader = DataLoader(dataset_test, batch_size=batch_size, shuffle = True)

    results = {"train_loader" : train_loader, "test_loader" : test_loader}

    torch.save(results, "data/processed/"+ "processed_tensor.pt")



