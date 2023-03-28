from time import time

class Counter(object):
    def __init__(self):
        """
        Useful class to get fps with librarias that don't have fps counter built-in.\n
        Methods
        -------
        - ``start()`` : set start time for the counter
        - ``stop()`` : set end time for the counter
        - ``get_fps()`` : calculate the fps based on start and end time\n
        Example
        -------
        >>> counter = FPSCounter()
        >>>
        >>> while True:
        >>>     counter.start()
        >>>     # do task
        >>>     counter.stop()
        >>>     print(get_fps())
        """
        self.start_time = None
        self.end_time = None
        self.fps_mean = 0
        self.fps_tot = 0
        self.max_fps = 0
        self.min_fps = 10^5
        self.i = 0

    def start(self):
        """
        Set start time for the counter.\n
        Set BEFORE an event start in a loop cycle!\n
        Example
        -------
        >>> counter = FPSCounter()
        >>>
        >>> while True:
        >>>     counter.start()
        >>>     # do task
        >>>     counter.stop()
        >>>     print(get_fps())
        """
        self.start_time = time()

    def stop(self):
        """
        Set end time for the counter.\n
        Set AFTER an event start in a loop cycle!\n
        Example
        -------
        >>> counter = FPSCounter()
        >>>
        >>> while True:
        >>>     counter.start()
        >>>     # do task
        >>>     counter.stop()
        >>>     print(get_fps())
        """
        self.end_time = time()

    def get_fps(self, get_stats=False, print_output=False, format_text=True):
        """
        Calculate the fps based on start and end time.\n
        Parameters
        ----------
        - ``get_stats`` : get fps_mean, max_fps and min_fps (default=False)
        - ``print_output`` : print fps on terminal (default=False)
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
        >>> counter = FPSCounter()
        >>>
        >>> while True:
        >>>     counter.start()
        >>>     # do task
        >>>     counter.stop()
        >>>     print(get_fps())
        """
        if self.start_time is None or self.end_time is None:
            print('[FPSCounter] Start time or end time not setted properly!')
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
            print(f"[FPSCounter] fps : {fps}")
            if get_stats:
                print(f"[FPSCounter] fps mean : {self.fps_mean}")
                print(f"[FPSCounter] Max fps  : {self.max_fps}")
                print(f"[FPSCounter] min fps  : {self.min_fps}")

        results = {
            'fps'  : fps           ,
            'mean' : self.fps_mean ,
            'max'  : self.max_fps  ,
            'min'  : self.min_fps
        }

        if get_stats:
            return results
        else:
            return results['fps']

    def _get_stat(self, fps):
        """
        Calculate fps_mean, max_fps, min_fps.
        """
        self.i += 1
        self.fps_tot += fps
        self.fps_mean = self.fps_tot/self.i
        if fps > self.max_fps:
            self.max_fps = fps
        if fps < self.min_fps:
            self.min_fps = fps

    def reset(self):
        """
        Reset the counter and all its attributes.
        """
        self.fps_mean = 0
        self.fps_tot = 0
        self.max_fps = 0
        self.min_fps = 10^5
        self.i = 0