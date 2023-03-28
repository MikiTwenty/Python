from time import time

class FPS_Counter():
    def __init__(self):
        '''
        Useful class to get fps with librarias that don't have fps counter built-in.\n
        Functions:
        - start()   : set start time for the counter
        - stop()    : set end time for the counter
        - get_fps() : calculate the fps based on start and end time
        '''
        self.start_time = None
        self.end_time = None
        self.fps_mean = 0
        self.fps_tot = 0
        self.fps_max = 0
        self.fps_min = 10^5
        self.i = 0

    def start(self):
        '''
        Set start time for the counter.\n
        Set BEFORE an event start in a loop cycle!
        '''
        self.start_time = time()

    def stop(self):
        '''
        Set end time for the counter.\n
        Set AFTER an event start in a loop cycle!
        '''
        self.end_time = time()

    def get_fps(self, getStats=False, printOutput=False, formatText=True):
        '''
        Calculate the fps based on start and end time.\n
        Parameters:
        - printOutput : print fps on terminal (default=False)
        - formatText  : return text as string with 2 decimals (default=True)
        '''
        if self.start_time is None or self.end_time is None:
            print('[FPS Counter] <Warning>: Start time or end time not setted properly!')
            return
        self.diff_time = self.end_time - self.start_time
        fps = 1 / self.diff_time
        self.start_time = self.end_time
        self.__get_stat(fps)

        if formatText:
            fps = float("{:.2f}".format(fps))
            self.fps_mean = float("{:.2f}".format(self.fps_mean))
            self.fps_max = float("{:.2f}".format(self.fps_max))
            self.fps_min = float("{:.2f}".format(self.fps_min))

        if printOutput:
            print("[FPS Counter] >> fps  :", fps)
            if getStats:
                print("[FPS Counter] >> mean :", self.fps_mean)
                print("[FPS Counter] >> Max  :", self.fps_max)
                print("[FPS Counter] >> min  :", self.fps_min)

        results = {
            'fps'  : fps           ,
            'mean' : self.fps_mean ,
            'max'  : self.fps_max  ,
            'min'  : self.fps_min
        }

        if getStats:
            return results
        else:
            return results['fps']

    def __get_stat(self, fps):
        self.i += 1
        self.fps_tot += fps
        self.fps_mean = self.fps_tot/self.i
        if fps > self.fps_max:
            self.fps_max = fps
        if fps < self.fps_min:
            self.fps_min = fps

    def reset(self):
        '''
        Reset the counter and all its attributes.
        '''
        self.fps_mean = 0
        self.fps_tot = 0
        self.fps_max = 0
        self.fps_min = 10^5
        self.i = 0