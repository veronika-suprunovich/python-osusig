from flask import Flask, render_template, request, send_file
import sigGenerator
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def generatedImage():
    username = request.args.get("uname", "tryonelove")
    color = request.args.get("color")
    sig = sigGenerator.OsuSig((187, 17, 119), username)
    sig.generateImage()
    return render_template("index.html")