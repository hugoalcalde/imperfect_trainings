from monai.networks.nets import densenet121
from monai.engines import SupervisedTrainer
import logging
import torch 
import sys
import random
import copy

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def change_labels (labels, percentage, random_seed):
    new_labels=labels
    random.seed(random_seed)
    num_images=len(labels)
    x = int(percentage * num_images) # Number of images to change
    one_indices=[]
    for index, label in enumerate(labels):
        if label==1:
            one_indices.append(index) #indices where the labels=1
    indices_to_change = random.sample(one_indices, x) 
    new_labels[indices_to_change] = 0 
    return new_labels


def calculate_accuracy(logits, targets):
    """Calculate the accuracy"""
    # Get predicted class indices
    predicted_indices = torch.argmax(logits, dim=1)
    
    # Compare with ground truth
    correct_predictions = (predicted_indices == targets).sum().item()
    
    # Calculate accuracy
    accuracy = correct_predictions / targets.size(0)
    
    return accuracy


# Model Definition : 
model = densenet121(spatial_dims=2, in_channels=1, out_channels=2).to("cpu")

# Training parameters : 
lr = 0.001
loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr)
max_epochs = 1
device = "cpu"
percentage = 0.1
seed_value=42

#Change labels of x% of the images from 1 to 0
processed_tensor= torch.load("data/processed/processed_tensor.pt")
train_data_loader = processed_tensor["train_loader"]

for epoch in range(max_epochs):
    model.train()
    epoch_loss = 0
    step = 0 
    epoch_loss_values = []
    for batch_data in train_data_loader:
        step += 1 
        inputs, labels = batch_data[0].to(device), batch_data[1].to(device)

        #change a percentage of labels from 1 to 0
        labels = change_labels (labels, percentage, seed_value)
            
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
