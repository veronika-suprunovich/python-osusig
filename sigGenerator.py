from PIL import Image, ImageDraw, ImageFont
import api
from config import API_KEY

class OsuSig:
    def __init__(self, color, username, mode=0):
        self.color = color
        self.mode = mode
        self.username = username
        self.img = Image.new("RGBA", (330, 86), color=color)
        self.API = api.BanchoApi(API_KEY)

    def generateImage(self):
        draw = self.drawImage()
        self.drawSigArea(draw)
        self.saveImage()

    def drawSigArea(self, draw):
        draw.rectangle((3, 35, 327, 82), fill="white")

    def saveImage(self):
        self.img.save("img.png")

    def setFont(self, image, x, y):
        fnt = ImageFont.truetype("./fonts/exo2medium.ttf", 10)
        image.text((30,30), "Hello world", font=fnt, fill=(255, 255, 0))

    def drawImage(self):
        i = ImageDraw.Draw(self.img)
        return i
    
    
