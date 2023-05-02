import sys, os
from pathlib import Path

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    Do not use path starting with './' . For example:
        Do not use './view/ui/main.ui' when calling this method, instead use 'view/ui/main.ui'.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        
    except Exception as e:
        base_path = os.path.abspath(".")

    native_relative_path = str(Path(relative_path))
    full_path = os.path.join(base_path, native_relative_path)
    return full_path.replace('\\', '/')