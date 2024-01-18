from tests import _PATH_DATA
import torch
import pytest
import os


#@pytest.mark.skipif(not os.path.exists(processed_tensor), reason="Data files not found")

def test_sets_dimmensions():
    processed_tensor = torch.load(_PATH_DATA + "processed_tensor.pt")

    
    train_dataloader = len(processed_tensor["train_loader"].dataset)
    test_dataloader = len(processed_tensor["test_loader"].dataset)

    print(train_dataloader)

    N = 200

    assert train_dataloader > test_dataloader, "Test set is bigger than train set"
    assert train_dataloader + test_dataloader  == N, "There was some data leak in the processing"

    