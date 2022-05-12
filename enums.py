from enum import Enum


class PythonVersionEnum(Enum):
    """
    possible value for `python_version`
    """
    DEFAULT = "default"
    PYTHON_37 = "3.7"
    PYTHON_38 = "3.8"
    PYTHON_39 = "3.9"