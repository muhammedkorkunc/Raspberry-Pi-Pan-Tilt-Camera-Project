import os
import threading
import socket
from flask import Flask, Response
from camera_pi import Camera

app = Flask(__name__)

# Servo control
pan_pin = 27
tilt_pin = 22
servo_script = "/home/fsm/servoCameraKontrol/angleServoCtrl.py"

# TCP server details
TCP_HOST = '0.0.0.0'
TCP_PORT = 65433

# ==== Video Streaming ====
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# ==== TCP Server for Servo Control ====
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            parts = data.strip().split(',')
            if len(parts) == 2:
                direction, angle = parts[0], int(parts[1])
                if direction == 'pan':
                    os.system(f"python3 {servo_script} {pan_pin} {angle}")
                elif direction == 'tilt':
                    os.system(f"python3 {servo_script} {tilt_pin} {angle}")
            conn.sendall(b"OK")
    finally:
        conn.close()

def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TCP_HOST, TCP_PORT))
        s.listen()
        print(f"TCP Server listening on {TCP_HOST}:{TCP_PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

# ==== Main Entrypoint ====
if __name__ == '__main__':
    threading.Thread(target=start_tcp_server, daemon=True).start()
    app.run(host='172.31.1.13', port=8080, debug=False, threaded=True)
