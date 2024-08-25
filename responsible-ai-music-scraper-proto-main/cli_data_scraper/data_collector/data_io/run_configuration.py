from dataclasses import dataclass


@dataclass
class RunConfiguration:
    """
    A class that represents a run configuration for a backend
    """
    # A list of backend ids with their name and arguments in a tuple
    backend_arguments: {str: (str, str)}
