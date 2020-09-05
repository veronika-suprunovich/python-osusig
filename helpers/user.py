from . import api
from config import API_KEY
from . import exceptions
import numpy

def formatAccuracy(num):
    num = round(float(num), 2)
    if num.is_integer():
        return round(num)
    return num

class User(dict):
    def __init__(self, uname, mode):
        self.uname = uname
        self.mode = mode
        self.getUserStats()

    def getUserStats(self):
        API = api.BanchoApi(API_KEY)
        try:
            self.user = API.get_user(u=self.uname, m=self.mode)[0]
        except IndexError:
            raise exceptions.UserNotFound
        self.user["accuracy"] = str(formatAccuracy(self.user["accuracy"]))

    def __getattr__(self, attr):
        return self.user.get(attr)
