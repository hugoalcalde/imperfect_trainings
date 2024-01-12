from monai.networks.nets import densenet121
from monai.engines import SupervisedTrainer
import logging
import torch 
import sys


def calculate_accuracy(logits, targets):
    # Get predicted class indices
    predicted_indices = torch.argmax(logits, dim=1)
    
    # Compare with ground truth
    correct_predictions = (predicted_indices == targets).sum().item()
    
    # Calculate accuracy
    accuracy = correct_predictions / targets.size(0)
    
    return accuracy




logging.basicConfig(stream=sys.stdout, level=logging.INFO)
train_data_loader = torch.load("data/processed/processed_tensor.pt")["train_loader"]

# Model Definition : 

model = densenet121(spatial_dims=2, in_channels=1, out_channels=2).to("cpu")


# Training parameters : 


lr = 0.001
loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr)
max_epochs = 5
device = "cpu"


for epoch in range(max_epochs):

    model.train()
    epoch_loss = 0
    step = 0 
    epoch_loss_values = []
    for batch_data in train_data_loader:
        step += 1 
        inputs, labels = batch_data[0].to(device), batch_data[1].to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_function(outputs, labels)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
        print("epoch_loss from step {} is {}".format(step, loss.item()))
        print("Accuracy {}".format(calculate_accuracy(outputs,labels)))
    epoch_loss /= step
    epoch_loss_values.append(epoch_loss)
    print(f"epoch {epoch + 1} average loss: {epoch_loss:.4f}")
torch.save(model.state_dict(), 'models/first_trial.pth')
