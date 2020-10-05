'''
Created on Monday, 5th October 2020 3:51::49 pm
@author: mtc-20
 Coded on VS Code 2019
------
Overview:
 References
 https://stackoverflow.com/a/54787912
 https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/7
------
Last Modified: Mon Oct 05 2020
'''
from flask import Flask, Response, jsonify, render_template
from camera import VideoCam
import cv2


app = Flask(__name__, template_folder='templates')

video_stream = VideoCam()

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run()
