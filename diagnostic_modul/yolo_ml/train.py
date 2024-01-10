from ultralytics import YOLO
import os
# from multiprocessing import freeze_support
if __name__ == '__main__':
    # freeze_support()
    # Load a model
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" # Убирате следующую ошибку: OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
    model = YOLO('yolov8x.yaml') # build a new model from YAML
    model = YOLO('yolov8x.pt')  # load a pretrained model (recommended for training)
    model = YOLO('yolov8x.yaml').load('yolov8x.pt')  # build from YAML and transfer weights

    # Train the model
    results = model.train(data='coco.yaml', epochs=50, imgsz=413)
    