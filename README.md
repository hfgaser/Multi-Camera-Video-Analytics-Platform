# Multi-Camera-Video-Analytics-Platform
📂 Project Structure

video_analytics_project/ ├── multi_stream.py # Main script with multi-camera, YOLOv5, Flask & MQTT ├── requirements.txt # Dependencies ├── README.md # Project description (this file) └── static/ # For potential frontend assets (optional)

🔧 Setup Instructions

Clone the Repo
git clone https://github.com/hfgaser/Multi-Camera-Video-Analytics-Platform.git

cd video-analytics-project

Install Dependencies
pip install -r requirements.txt

If requirements.txt is not yet generated, install manually:

pip install opencv-python flask torch torchvision yolov5 pandas paho-mqtt

(Optional) MQTT Broker Setup
Use test.mosquitto.org or install Mosquitto locally.

🎞️ Run the Application

python multi_stream.py

Default Endpoints:

GET /start/cam1 ➔ Start webcam

GET /start/cam2 ➔ Start iPhone/IP stream

GET /video_feed/cam1 ➔ MJPEG stream for cam1

GET /stop/cam1 ➔ Stop webcam

📊 Credits

Created for CMP4221 - Multimedia Systems & Communications
By: Hasan Furkan Gaser
    Kerem Çakıllı 
    Mehmet Selim
