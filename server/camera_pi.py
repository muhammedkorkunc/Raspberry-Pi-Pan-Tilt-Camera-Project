"""
Dual-Axis Pan-Tilt Camera Controller - Web Server Entrypoint

Author: Muhammed Emin Korkunç (muhammedemin.korkunc@gmail.com | https://github.com/muhammedkorkunc)
Collaborators: Nurettin Süleymanoğlu, Faruk Kerem Bedir
Date: 2026-09-26
Description: Flask server handling HTTP routes, video feeds, and remote servo telemetry.
"""

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
