import subprocess

# Get the actual path to the processed_tensor.pt file
data_path = subprocess.check_output(['dvc', 'path', 'processed/processed_tensor.pt']).decode('utf-8').strip()

print(f"Using data from: {data_path}")