import cv2
import torch
from flask import Flask, Response, jsonify
import threading

app = Flask(__name__)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.4

# Kamera listesi (webcam veya IP)
CAMERA_SOURCES = {
    'cam1': 0,  # 0 = default webcam
    'cam2': "http://192.168.1.140:4747/video"  # Örnek RTSP
}

running = {}
caps = {}
frames = {}
locks = {}

# Her kamera için ayrı stream thread
def stream_loop(name):
    global running, caps, frames
    while running.get(name, False):
        ret, frame = caps[name].read()
        if not ret:
            continue
        results = model(frame)
        annotated = results.render()[0]
        with locks[name]:
            frames[name] = annotated

# MJPEG üretici
def generate_stream(name):
    while True:
        with locks[name]:
            if name not in frames or frames[name] is None:
                continue
            _, buffer = cv2.imencode('.jpg', frames[name])
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/start/<cam_id>')
def start_cam(cam_id):
    if cam_id not in CAMERA_SOURCES:
        return jsonify({"status": "invalid camera"})

    if running.get(cam_id):
        return jsonify({"status": "already running"})

    caps[cam_id] = cv2.VideoCapture(CAMERA_SOURCES[cam_id])
    if not caps[cam_id].isOpened():
        return jsonify({"status": "camera open failed"})

    frames[cam_id] = None
    locks[cam_id] = threading.Lock()
    running[cam_id] = True

    threading.Thread(target=stream_loop, args=(cam_id,), daemon=True).start()
    return jsonify({"status": f"{cam_id} started"})

@app.route('/stop/<cam_id>')
def stop_cam(cam_id):
    running[cam_id] = False
    if cam_id in caps:
        caps[cam_id].release()
    return jsonify({"status": f"{cam_id} stopped"})

@app.route('/video_feed/<cam_id>')
def video_feed(cam_id):
    if cam_id not in CAMERA_SOURCES:
        return jsonify({"status": "invalid camera"})
    return Response(generate_stream(cam_id), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
