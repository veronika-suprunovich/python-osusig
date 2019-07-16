from flask import Flask, render_template
from PIL import Image, ImageDraw
import sigGenerator

app = Flask(__name__)

@app.route("/")
def hello():
    sig = sigGenerator.OsuSig((187, 17, 119), "tryonelove")
    sig.generateImage()
    return render_template("index.html")