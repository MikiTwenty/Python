from torch import cuda as CUDA
from ultralytics import YOLO

class Model(YOLO):
    def __init__(self, YOLO_model, YOLO_task=None, YOLO_session=None):
        super().__init__(model=YOLO_model, task=YOLO_task, session=YOLO_session)
        try:
            if not CUDA.is_available():
                print(f"[YOLOv8] CUDA not avaible!")
            else:
                try:
                    if not CUDA.is_initialized():
                        CUDA.init()
                    print(f"[YOLOv8] CUDA initialized")
                    try:
                        CUDA.empty_cache()
                        print("[YOLOv8] CUDA cache cleared")
                    except Exception as error:
                        raise(error)
                except Exception as error:
                    raise(error)
        except Exception as error:
            raise(error)

    def process_image(self, frame, confidence=0.6, max_objects_detected=10):
        results = self.predict(
            source       = frame      ,
            #classes      = [0]        ,
            show         = False      ,
            conf         = confidence ,
            retina_masks = True       ,
            max_det      = max_objects_detected
        )
        processed_frame = results[0].plot()
        return processed_frame