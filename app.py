from flask import Flask, render_template, request, send_file, make_response
import sigGenerator
import os
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    username = request.args.get("uname", "tryonelove")
    color = request.args.get("color")
    sig = sigGenerator.OsuSig((187, 17, 119), username)
    sig.generateImage()
    return render_template("index.html")


@app.route("/sig")
def generatedImage():
    username = request.args.get("uname", "tryonelove")
    color = request.args.get("color")
    sig = sigGenerator.OsuSig((187, 17, 119), username)
    sig.generateImage()
    path = os.path.join('static', 'sig.png')
    return send_file(path, mimetype="image/png")