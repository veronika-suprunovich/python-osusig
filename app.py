from flask import Flask, render_template, request, send_file, make_response
import sigGenerator
import os
from io import BytesIO
import config

app = Flask(__name__)

def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

@app.route("/")
def index():
    return render_template("index.html", sigPicture="/sig")

@app.route("/sig") 
def generatedImage():
    username = request.args.get("uname", "tryonelove")
    color = request.args.get("colour", "darkpink")
    mode = request.args.get("mode", "0")
    showPP = request.args.get("pp", -1)
    if color in config.DEFAULT_COLORS.keys():
        color = config.DEFAULT_COLORS.get(color)
    color = hex_to_rgb(color)
    sig = sigGenerator.OsuSig(
        color, username, mode, showPP)
    sig.generateImage()
    path = os.path.join('static', 'sig.png')
    return send_file(path, mimetype="image/png")