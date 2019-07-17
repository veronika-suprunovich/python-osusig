from PIL import Image, ImageDraw, ImageFont
import api
from config import API_KEY
import requests
import os


MODE = {
    0 : "osu",
    1 : "taiko",
    2 : "ctb",
    3 : "mania"
}


class OsuSig:
    def __init__(self, color, username, mode=0):
        self.img = Image.new("RGBA", (330, 86), color=color)
        self.color = color
        self.username = username
        self.mode = MODE.get(mode)
        self.API = api.BanchoApi(API_KEY)
        self.getUserStats()

    def getUserStats(self):
        user = self.API.get_user(u=self.username)[0]
        self.username = user["username"]
        self.user_id = user["user_id"]
        self.rank = int(user["pp_rank"])
        self.country = user["country"]

    def generateImage(self):
        draw = self.drawImage()
        self.drawSigArea(draw)
        avatar = self.getUserAvatar()
        self.drawAvatar(avatar)
        # draw username
        self.drawText(self.username, (86, 7), draw, "exo2bold", 20, (255,255,255))
        # draw rank
        self.drawText("#{}".format(self.rank), (269 - self.moveRank(), 15), draw, "exo2regular", 13, (255,255,255))
        self.drawFlag()
        self.drawMode()
        self.saveImage()

    def moveRank(self):
        if self.rank < 10:
            return 0
        rank = str(self.rank)
        return len(rank) * 5.7

    def drawSigArea(self, draw):
        draw.rectangle((3, 35, 327, 82), fill="white")

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
        flag = Image.open("flags/{}.png".format(self.country))
        flag = flag.resize((18, 12), Image.ANTIALIAS)
        self.img.paste(flag, (303, 17), flag)

    def getUserAvatar(self):
        avatar_url = "https://a.ppy.sh/{}_.jpg".format(self.user_id)
        r = requests.get(avatar_url, stream=True)
        if r.status_code == 200:
            with open("avatar.jpg", 'wb') as f:
                f.write(r.content)
        avatar = Image.open("avatar.jpg")
        return avatar

    def drawAvatar(self, avatar):
        resize_ratio = avatar.size[0] / avatar.size[1]
        new_size_x = 76
        new_size_y = int(new_size_x * resize_ratio)
        avatar = avatar.resize((new_size_x, new_size_y), Image.ANTIALIAS)
        self.img.paste(avatar, (5,5))
        
    def saveImage(self):
        self.img.save("./static/sig.png")
    
    

