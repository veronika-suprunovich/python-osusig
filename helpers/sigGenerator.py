from PIL import Image, ImageDraw, ImageFont
from . import api
from config import API_KEY
import requests
import os
from .user import User
import io

MODE = {
    "0" : "osu",
    "1" : "taiko",
    "2" : "ctb",
    "3" : "mania"
}

class OsuSig:
    def __init__(self, 
                color, username,
                mode=0, 
                showPP = None, 
                showRankedScore = False,
                showXPBar = False,
                isCountryRank = False):
        self.img = Image.new("RGB", (330, 86), color=color)
        self.color = color
        self.user = User(username, mode)
        self.mode = MODE.get(mode)
        self.showPP = showPP
        self.showRankedScore = showRankedScore
        self.showXPBar = showXPBar
        self.isCountryRank = isCountryRank

    def __repr__(self):
        return self.img

    def serverImage(self):
        img_io = io.BytesIO()
        self.img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io

    def generateImage(self):
        draw = self.drawImage()
        self.drawSigArea(draw)
        avatar = self.getUserAvatar()
        self.drawAvatar(avatar)
        self.drawUsername(draw)
        self.drawRank(draw)
        self.drawAccuracy(draw)
        self.drawRankedScore(draw) if self.showRankedScore else self.drawPlaycount(draw)
        self.drawFlag()
        self.drawMode()
        return self.serverImage()

    def fontCoords(self, draw, font, text, size, coords):
        fnt = ImageFont.truetype("./fonts/{}.ttf".format(font), size)
        text_size = draw.textsize(text, font=fnt)
        return (coords[0] - text_size[0], coords[1])

    def getFontSize(self, text):
        if len(text)>10:
            return 23 - (len(text) // 10)
        return 24

    def drawUsername(self, draw):
        size = self.getFontSize(self.user.username)
        self.drawText(self.user.username, 
            (86, 3) if size == 24 else (86,5),
            draw, "exo2medium", size, (255,255,255))
    
    def drawRank(self, draw):
        text = "#{}".format(self.user.pp_rank)
        coords  = self.fontCoords(draw, "exo2regular", text, 14, (280, 14))
        self.drawText(
            text, 
            coords,
            draw, 
            "exo2regular",
            14,
            (255,255,255)
        )

    def drawAccuracy(self, draw):
        if self.showPP=="1":
            text, base_coords = '{} ({}pp)'.format(self.user.accuracy +"%", round(float(self.user.pp_raw))), (319, 37)
        else:
            text, base_coords = '{}'.format((self.user.accuracy +"%")), (315, 37)
        coords  = self.fontCoords(draw, "exo2regular", text, 14, base_coords)
        self.drawText("Accuracy", (87, 38), draw, "exo2regular", 14, (85, 85, 85))
        self.drawText(text, coords, draw, "exo2bold", 14, (85, 85, 85))

    def drawPlaycount(self, draw):
        self.drawText("Play Count", (87, 55), draw, "exo2regular", 14, (85, 85, 85))
        text = ""
        if self.showPP=="0":
            text, base_coords = '{0:,} ({1}pp)'.format(int(self.user.playcount), round(float(self.user.pp_raw))), (319, 55)
        else:
            text, base_coords = '{0:,} (lv{1})'.format(int(self.user.playcount), round(float(self.user.level))), (319, 55)
        coords  = self.fontCoords(draw, "exo2bold", text, 14, base_coords)
        self.drawText(text, 
                    coords, 
                    draw, 
                    "exo2bold", 
                    14,
                    (85, 85, 85))

    def drawRankedScore(self, draw):
        self.drawText("Ranked Score", (87, 55), draw, "exo2regular", 14, (85, 85, 85))
        self.drawText("{0:,}".format(int(self.user.ranked_score)), (273, 54), draw, "exo2bold", 14, (85, 85, 85))

    def moveRegular(self, text):
        text = str(text)
        return len(text) - 1

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
        self.img.paste(
                mode, 
                (286, 17), 
                mode)

    def drawFlag(self):
        flag = Image.open("flags/{}.png".format(self.user.country))
        flag = flag.resize((18, 13), Image.ANTIALIAS)
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
        resize_ratio = avatar.size[0] / avatar.size[1]
        new_size_y = 76
        new_size_x = int(new_size_y * resize_ratio)
        avatar = avatar.resize((new_size_x, new_size_y), Image.ANTIALIAS)
        self.img.paste(avatar, (5,5))

    def saveSig(self):
        self.img.save("static/sig.png")
    

