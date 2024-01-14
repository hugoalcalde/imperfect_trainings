from fastapi import FastAPI, UploadFile, File
from http import HTTPStatus
import torch
from torchvision import transforms
from torchvision.io import read_image, ImageReadMode
from torch.nn import Softmax
from monai.networks.nets import densenet121



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
    return "Probablity of Hemorrhage {}".format(logits.detach().numpy()[0][1])
    predicted_indices = torch.argmax(logits, dim=1)
    if predicted_indices == 1:
        return "Hemorrhage"
    else:
        return "Normal"

@app.post("/model/")
async def cv_model(data: UploadFile = File(...)):
    content = await data.read()
    content
    filename = data.filename
    predictions = classify_image("../data/raw/head_ct/"+filename)

    response = {
        "input": data.filename,
        "predictions": predictions,
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response