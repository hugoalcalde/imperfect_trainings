import pandas as pd 
from torchvision.io import read_image, ImageReadMode
import torch 
import os 

def qa_measure(image) : 
    return torch.mean(image), image.shape


data_path = "../Data/raw/head_ct/"
list_images = os.listdir(data_path)
list_images  = [data_path + x for x in list_images]

list_means = []
list_x = []
list_y = []

for image in list_images: 
    img = read_image(image, mode = ImageReadMode.GRAY ).type(torch.float32)
    mean, shape = qa_measure(img)

    list_means.append(mean)
    list_x.append(shape[1])
    list_y.append(shape[2])


reference_df = pd.DataFrame()
reference_df["mean"] = [float(x) for x in list_means]
reference_df["image_x"] = list_x
reference_df["image_y"] = list_y


reference_df.to_csv("reference_database.csv", index = False)
