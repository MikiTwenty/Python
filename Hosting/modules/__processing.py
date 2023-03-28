import torch
from ultralytics import YOLO

class Model(object):
    def __init__(self, yolo_model):
        # set model to use
        self.model = YOLO(yolo_model)

        # check if CUDA is avaible
        if not torch.cuda.is_available():
            print("CUDA not avaible!")
            exit()

        # check if CUDA is initialized
        if not torch.cuda.is_initialized:
            print("CUDA not initialized!")
            exit()

        torch.cuda.empty_cache()

    def process(self, frame, confidence=0.6, max_objects_detected=10, getOutput=False):
        # use the model to predict directly on the video frame
        results = self.model.predict(
            source       = frame      ,          # image to process (can be a video flow)
            #classes      = [0]        ,         # classes to detect (see coco128.yaml)
            show         = getOutput  ,          # get video output
            conf         = confidence ,          # accuracy threshold
            max_det      = max_objects_detected  # max number of object detected (large numbers impact on performance)
        )

        processed_frame = results[0].plot()

        return processed_frame