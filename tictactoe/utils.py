"""Script with helper functions."""
import pathlib
import torch


def load_checkpoint(model: torch.nn.Module, args) -> None:
    """Loads model from checkpoint.

    Args:
        model: PyTorch model.
        model_name: Name of policy model.
        args: Parsed arguments.
    """
    model_name = args["model_name"]
    algorithm_name = args["algorithm"]
    checkpoint_name = f"{f'{model_name}_{algorithm_name}' if model_name else 'model'}"
    checkpoint_path = "weights"
    model_path = pathlib.Path(checkpoint_path) / f"{checkpoint_name}.pth"

    if model_path.is_file():
        state_dict = torch.load(f=model_path)
        #print(state_dict['model.1.weight'].tolist());
        model.load_state_dict(state_dict=state_dict)
        print(f"\nModel '{checkpoint_name}' loaded.")
    else:
        print("model was not read successfully.")