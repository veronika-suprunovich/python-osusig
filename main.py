from flask import Flask, render_template, request
import sigGenerator

app = Flask(__name__)

@app.route("/sig")
def hello():
    username = request.args.get("uname")
    color = request.args.get("color")
    sig = sigGenerator.OsuSig((187, 17, 119), username)
    sig.generateImage()
    return render_template("index.html")