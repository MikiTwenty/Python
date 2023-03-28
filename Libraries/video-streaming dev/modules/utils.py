import os
from random import randint

def get_cwd(dir):
    """
    Get current work directory.\n
    Parameters
    ----------
    - ``dir`` (str): directory to set,
    pass ``__file__`` to set the directory of the file you have call this method.
    """
    os.chdir(os.path.dirname(os.path.abspath(dir)))

def clear_output():
    """
    Clear terminal output.
    """
    os.system("cls")

def get_RGB(color):
    """
    Return predefined colors in rgb format.\n
    Parameters
    ----------
    - ``color`` (str): can be 'red', 'green', 'blue', 'black', 'white'
     or 'random' to generate a casual rgb color code.\n
    Returns
    -------
    - ``tuple`` (int, int, int): rgb format color.
    """
    RGBcolors = {
        "red" : (255, 0, 0),
        "green" : (0, 255, 0),
        "blue" : (0, 0, 255),
        "black" : (0, 0, 0),
        "white" : (255, 255, 255),
        "random" : (randint(0, 255), randint(0, 255), randint(0, 255))
    }
    return RGBcolors[color]