from monai.networks.nets import densenet121
import logging
import torch 
import sys
import hydra
import os 
import matplotlib.pyplot as plt 
from hydra.utils import instantiate


def calculate_accuracy(logits, targets):
    # Get predicted class indices
    predicted_indices = torch.argmax(logits, dim=1)
    
    # Compare with ground truth
    correct_predictions = (predicted_indices == targets).sum().item()
    
    # Calculate accuracy
    accuracy = correct_predictions / targets.size(0)
    
    return accuracy


log = logging.getLogger(__name__)


@hydra.main(config_name="config_train.yaml")
def train(config) : 

    # Get the original working directory
    original_wd = hydra.utils.get_original_cwd()

    # Change back to the original working directory
    os.chdir(original_wd)
    data_path = config["data_path"]
    train_loader = torch.load(data_path)["train_loader"]
    test_loader = torch.load(data_path)["test_loader"]


    # Model Definition : 

    model = densenet121(spatial_dims=2, in_channels=1, out_channels=2).to("cpu")

    # Training parameters : 

    lr = float(config["learning_rate"])
    training_name = config["training_name"]
    loss_function =  instantiate(config["loss_function"])
    optimizer = instantiate(config["optimizer"], model.parameters(), lr = lr)
    num_epochs = int(config["epochs"])



    loss_list = []
    train_accuracy = []
    test_accuracy = []

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        running_acc = 0.0

        for inputs, labels in train_loader:
            optimizer.zero_grad()  # Zero the gradients
            outputs = model(inputs)  # Forward pass
            loss = loss_function(outputs, labels)  # Compute the loss
            loss.backward()  # Backward pass
            optimizer.step()  # Update the weights
            train_acc = calculate_accuracy(outputs, labels)
            running_loss += loss.item()
            running_acc += train_acc

        average_loss = running_loss / len(train_loader)
        average_accuracy = running_acc / len(train_loader)

        loss_list.append(average_loss)
        train_accuracy.append(average_accuracy)
        running_test_acc = 0.0
        for inputs, labels in test_loader:
            preds = model(inputs)
            test_acc = calculate_accuracy(preds, labels)
            running_test_acc += test_acc
        average_test_accuracy = running_test_acc / len(test_loader)
        test_accuracy.append(average_test_accuracy)
        log.info(f"Epoch {epoch + 1}/{num_epochs}, Loss: {average_loss:.4f}, Train Accuracy : {average_accuracy:.4f}, Test Accuracy : {average_test_accuracy:.4f}")
    
    plt.figure(figsize=(10, 5))
    plt.plot(train_accuracy, label='Train Accuracy', color='darkblue')
    plt.plot(test_accuracy, label='Test Accuracy', color='darkgreen')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title(f'Train and Test Accuracy')
    if not os.path.exists(f"reports/figures/{training_name}"):
        os.makedirs(f"reports/figures/{training_name}")
    plt.savefig(f"reports/figures/{training_name}/accuracy.png")
    plt.close()
    plt.plot(loss_list,color = "darkblue")
    plt.xlabel("Epochs")
    plt.ylabel("Training Loss")
    if not os.path.isdir("reports/figures/{}".format(training_name)):
        os.system("mkdir reports/figures/{}".format(training_name))
    plt.savefig("reports/figures/{}/training.png".format(training_name))
    plt.close()
    if not os.path.isdir("models/{}".format(training_name)):
        os.system("mkdir models/{}".format(training_name))
    torch.save(model.state_dict(), "models/{}/checkpoint.pth".format(training_name))

if __name__ == "__main__":
    train()