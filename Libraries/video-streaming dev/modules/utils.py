import os
from time import time
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

class Clock(object):
    def __init__(self):
        """
        Useful class to get fps with librarias that don't have fps Clock built-in.\n
        Methods
        -------
        - ``tick()`` : set start time for the Clock before an event starts.
        - ``get_fps()`` : calculate the fps of a loop cycle\n
        Example
        -------
        >>> clock = Clock()
        >>> while True:
        >>>     # do task
        >>>     clock.get_fps()
        """
        self.start_time = None
        self.end_time = None
        self.fps_mean = 0
        self.fps_tot = 0
        self.max_fps = 0
        self.min_fps = 10^5
        self.i = 0

    def tick(self):
        """
        Set start time for the Clock before an event starts.\n
        Example
        -------
        >>> clock = Clock()
        >>> while True:
        >>>     clock.start()
        >>>     # do task
        >>>     clock.get_fps()
        """
        self.start_time = time()

    def get_fps(self, get_stats=False, print_output=True, format_text=True):
        """
        Calculate the fps of a loop cycle.\n
        Parameters
        ----------
        - ``get_stats`` : get fps_mean, max_fps and min_fps (default=False)
        - ``print_output`` : print fps on terminal (default=True)
        - ``format_text`` : return values as string with 2 decimals (default=True)\n
        Returns
        -------
        - ``str`` : if format_text=True
        - ``float`` : if format_text=False
        - ``dict`` (vals: str) :
         if get_stats=True and format_text=True
        - ``dict`` (vals: float) :
         if get_stats=True and format_text=False\n
        Example
        -------
        >>> clock = Clock()
        >>> while True:
        >>>     # do task
        >>>     clock.get_fps()
        """
        self.end_time = time()

        if self.start_time is None or self.end_time is None:
            print('[Clock] Initialized')
            self.start_time = time()
            return

        self.diff_time = self.end_time - self.start_time
        fps = 1 / self.diff_time
        self.start_time = self.end_time
        self._get_stat(fps)

        if format_text:
            fps = float("{:.2f}".format(fps))
            self.fps_mean = float("{:.2f}".format(self.fps_mean))
            self.max_fps = float("{:.2f}".format(self.max_fps))
            self.min_fps = float("{:.2f}".format(self.min_fps))

        if print_output:
            print(f"[Clock] fps : {fps}")
            if get_stats:
                print(f"[Clock] fps mean : {self.fps_mean}")
                print(f"[Clock] Max fps  : {self.max_fps}")
                print(f"[Clock] min fps  : {self.min_fps}")

        results = {
            'fps'  : fps           ,
            'mean' : self.fps_mean ,
            'max'  : self.max_fps  ,
            'min'  : self.min_fps
        }

        self.start_time = self.end_time

        if get_stats:
            return results
        else:
            return results['fps']

    def _get_stat(self, fps):
        self.i += 1
        self.fps_tot += fps
        self.fps_mean = self.fps_tot/self.i
        if fps > self.max_fps:
            self.max_fps = fps
        if fps < self.min_fps:
            self.min_fps = fps