from dataclasses import dataclass
from datetime import datetime


@dataclass
class TextContainer:
    """
    A class that represents a container for text data.
    """
    creation_data: datetime
    text_table: {str: [str]}
