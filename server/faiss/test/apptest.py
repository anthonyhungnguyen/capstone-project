#!/usr/bin/env python
from importlib import import_module
import os
import cv2
from flask import Flask, render_template, Response

# import camera driver
import __init__
from test import PYTHON_PATH
from test.streamtest import Camera

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
        except Exception as e:
            print("Exception", e)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.1.6', port='8001', threaded=True)
