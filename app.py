# !/usr/bin/env python
import dash
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, Response
from plant_watcher.video import PiWebCam


def generate_frame(camera):
    while True:
        frame = camera.get_stream().get_value()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


server = Flask(__name__)
app = dash.Dash(__name__, server=server)


@server.route('/video_feed')
def video_feed():
    return Response(generate_frame(PiWebCam()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


app.layout = html.Div([
    html.H1("Webcam Test"),
    html.Img(src="/video_feed")
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
