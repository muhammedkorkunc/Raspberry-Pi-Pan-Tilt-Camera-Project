from picamera2 import Picamera2
import cv2

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(main={"format": "XRGB8888"}))
        self.picam2.start()

    def get_frame(self):
        frame = self.picam2.capture_array()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
