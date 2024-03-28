import cv2
from PIL import Image

class CameraEmulator:
    def __init__(self, video_file):
        self.video_file = video_file
        self.cap = cv2.VideoCapture(video_file)

    def get_frame(self) -> Image:
        ret, frame = self.cap.read()
        if ret:
            return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return None

    def release(self):
        self.cap.release()


