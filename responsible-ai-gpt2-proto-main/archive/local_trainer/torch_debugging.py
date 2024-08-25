import torch

# Check if CUDA is available
if torch.cuda.is_available():
    device = torch.device("cuda")
    current_device = torch.cuda.current_device()
    print("CUDA is available")

    # Print the current CUDA device
    print("Current CUDA device: ", current_device)    

    # Print the current CUDA device name
    print("Current CUDA device name: ", torch.cuda.get_device_name(current_device))

    # Get the number of CUDA devices
    print("Number of CUDA devices: ", torch.cuda.device_count())

# Check if cpu_adam cuda is available