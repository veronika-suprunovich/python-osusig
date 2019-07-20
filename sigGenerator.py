from PIL import Image, ImageDraw, ImageFont
import api
from config import API_KEY
import requests
import os
from user import User

MODE = {
    0 : "osu",
    1 : "taiko",
    2 : "ctb",
    3 : "mania"
}

class OsuSig:
    def __init__(self, color, username, mode=0):
        self.img = Image.new("RGB", (330, 86), color=color)
        self.color = color
        self.user = User(username, mode)
        self.mode = MODE.get(mode)

    def generateImage(self):
        draw = self.drawImage()
        self.drawSigArea(draw)
        avatar = self.getUserAvatar()
        self.drawAvatar(avatar)
        # draw username
        self.drawText(self.user.username, (86, 3), draw, "exo2medium", 24, (255,255,255))
        # draw rank
        self.drawText("#{}".format(self.user.pp_rank), 
            (269 - self.moveRank(), 15),
            draw, 
            "exo2regular",
            13,
            (255,255,255)
        )
        #draw accuracy
        self.drawText("Accuracy", (87, 38), draw, "exo2regular", 14, (85, 85, 85))
        self.drawText(self.user.accuracy.rjust(4) +"%", (273, 37), draw, "exo2bold", 14, (85, 85, 85))
        #draw playcount
        self.drawText("Play Count", (87, 55), draw, "exo2regular", 14, (85, 85, 85))
        self.drawText(self.user.playcount, (273, 54), draw, "exo2bold", 14, (85, 85, 85))
        self.drawFlag()
        self.drawMode()
        self.saveSig()

    def moveRank(self):
        if int(self.user.pp_rank) < 10:
            return 0
        rank = str(self.user.pp_rank)
        return len(rank) * 6

    def drawSigArea(self, draw):
        draw.rectangle((3, 35, 326, 82), fill="white")

    def drawText(self, text, coords, image, font_type, font_size, color):
        fnt = ImageFont.truetype("./fonts/{}.ttf".format(font_type), font_size)
        image.text(coords, text, font=fnt, fill=color)

    def drawImage(self):
        i = ImageDraw.Draw(self.img)
        return i

    def drawMode(self):
        mode = Image.open("img/{}.png".format(self.mode))
        mode = mode.resize((12, 12), Image.ANTIALIAS)
        self.img.paste(mode, (286, 17), mode)

    def drawFlag(self):
        flag = Image.open("flags/{}.png".format(self.user.country))
        flag = flag.resize((18, 12), Image.ANTIALIAS)
        self.img.paste(flag, (303, 17), flag)

    def getUserAvatar(self):
        avatar_url = "https://a.ppy.sh/{}_.jpg".format(self.user.user_id)
        r = requests.get(avatar_url, stream=True)
        if r.status_code == 200:
            with open("avatar.jpg", 'wb') as f:
                f.write(r.content)
        avatar = Image.open("avatar.jpg")
        return avatar

    def drawAvatar(self, avatar):
        # x 76
        # y 75
        resize_ratio = avatar.size[0] / avatar.size[1]
        new_size_y = 76
        new_size_x = int(new_size_y * resize_ratio)
        avatar = avatar.resize((new_size_x, new_size_y), Image.ANTIALIAS)
        self.img.paste(avatar, (5,5))

    def saveSig(self):
        self.img.save("static/sig.png")
    

