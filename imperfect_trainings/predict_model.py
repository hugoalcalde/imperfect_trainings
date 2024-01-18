from torch import nn 
import torch 
from monai.networks.nets import densenet121
import time 


def predict(
    model: torch.nn.Module,
    dataloader: torch.utils.data.DataLoader, 
    gpu : int
) -> None:

    """Run prediction for a given model and dataloader.
    
    Args:
        model: model to use for prediction
        dataloader: dataloader with batches
    
    Returns
        Tensor of shape [N, d] where N is the number of samples and d is the output dimension of the model

    """

    if gpu == 2 : 
        model = nn.DataParallel(model, device_ids=[0,1])
    elif gpu == 4 : 
        model = nn.DataParallel(model, device_ids=[0,1, 2,3])
    elif gpu == 8 : 
        model = nn.DataParallel(model, device_ids=[0,1, 2,3, 4, 5, 6, 7])

    return torch.cat([model(batch) for batch, label in dataloader], 0)

model = densenet121(spatial_dims=2, in_channels=1, out_channels=2)
model.load_state_dict(torch.load("models/baselinetraining/checkpoint.pth"))   
dataloader = torch.load("data/processed/processed_tensor.pt")["train_loader"]
for i in [0,2,4,8] : 

    start = time.time()
    prediction = predict(model, dataloader, i)
    end = time.time()

    print(f"The inference time using {i} gpus is {end-start}")
