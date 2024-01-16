from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from http import HTTPStatus
import torch
from torchvision import transforms
from torchvision.io import read_image, ImageReadMode
from torch.nn import Softmax
from monai.networks.nets import densenet121
from datetime import datetime


def qa_measure(image) : 
    return torch.mean(image), image.shape

with open("qa_database.csv", "w") as file:
    file.write("time,mean,image_x,image_y\n")

def add_to_database(
    now: str,
    mean : float, 
    image_x : int, 
    image_y : int
    
):
    """Simple function to add prediction to database."""
    with open("qa_database.csv", "a") as file:
        file.write(f"{now}, {mean}, {image_x}, {image_y}\n")

app = FastAPI()

@app.get("/")
def root():
    """ Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response


def classify_image(image_data):
    image = read_image(image_data, mode = ImageReadMode.GRAY ).type(torch.float32)
    mean_intensity, image_shape= qa_measure(image)

    transform_normalize = transforms.Compose([
        transforms.Resize(size=(90, 90), antialias=True),
        transforms.Normalize(mean=1, std=1)
    ])  
    image = transform_normalize(image).unsqueeze(0) 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = densenet121(spatial_dims=2, in_channels=1, out_channels=2).to(device)
    model.load_state_dict(torch.load("../models/wandb_test/checkpoint.pth"))    
    softmax = Softmax()
    logits = softmax(model(image.to(device)))
    return "Probablity of Hemorrhage {}".format(logits.detach().numpy()[0][1]), mean_intensity, image_shape

@app.post("/model/")
async def cv_model(backgrounds_tasks : BackgroundTasks, data: UploadFile = File(...)):
    content = await data.read()
    content
    filename = data.filename
    predictions, mean_intensity, image_shape= classify_image("../data/raw/head_ct/"+filename)

    response = {
        "input": data.filename,
        "predictions": predictions,
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }

    now = str(datetime.now())

    backgrounds_tasks.add_task(add_to_database,now, mean_intensity, image_shape[1], image_shape[2])
    return response