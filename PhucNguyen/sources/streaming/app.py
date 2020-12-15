#!/usr/bin/env python
from importlib import import_module
import os
import cv2
from flask import Flask, render_template, Response

# import camera driver
import __init__
from streaming import PYTHON_PATH
from streaming.camera_opencv_tracker_mail import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        try:
            frame = camera.get_frame()
        except:
            not_found = os.path.join(
                PYTHON_PATH, "ailibs", "testing", "images", "notfound.jpg")
            frame = cv2.imread(not_found)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.1.123', port='8001', threaded=True)
