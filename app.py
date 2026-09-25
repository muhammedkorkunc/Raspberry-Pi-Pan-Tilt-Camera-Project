"""
Dual-Axis Pan-Tilt Camera Controller - Web Server Entrypoint

Author: Muhammed Emin Korkunç (muhammedemin.korkunc@gmail.com | https://github.com/muhammedkorkunc)
Collaborators: Nurettin Süleymanoğlu, Faruk Kerem Bedir
Date: 2026-09-26
Description: Flask server handling HTTP routes, video feeds, and remote servo telemetry.
"""

from flask import Flask, render_template, redirect, url_for
import socket
from flask import Flask, render_template, jsonify

app = Flask(__name__)

TCP_HOST = '172.31.1.13'  # Change if appCam.py is on another device
TCP_PORT = 65433
VIDEO_HOST = '172.31.1.13'
VIDEO_PORT = 8080

# State tracking
pan_angle = 90
tilt_angle = 90
STEP = 15  # Change amount per click

def send_command(direction, angle):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_HOST, TCP_PORT))
            message = f"{direction},{angle}"
            s.sendall(message.encode())
            s.recv(1024)
    except ConnectionRefusedError:
        print("Could not connect to appCam TCP server.")

@app.route("/")
def index():
    return render_template("controller.html", video_url=f"http://{VIDEO_HOST}:{VIDEO_PORT}/video_feed")

@app.route("/pan/<dir>")
def pan(dir):
    global pan_angle
    if dir == "left":
        pan_angle = max(0, pan_angle - STEP)
    elif dir == "right":
        pan_angle = min(180, pan_angle + STEP)
    send_command('pan', pan_angle)
    return jsonify(status="ok")  # Don't redirect

@app.route("/tilt/<dir>")
def tilt(dir):
    global tilt_angle
    if dir == "up":
        tilt_angle = max(0, tilt_angle - STEP)
    elif dir == "down":
        tilt_angle = min(180, tilt_angle + STEP)
    send_command('tilt', tilt_angle)
    return jsonify(status="ok")  # Don't redirect

if __name__ == "__main__":
    app.run(debug=True)