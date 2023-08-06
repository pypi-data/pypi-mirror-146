from uuid import uuid4
import requests


api = "https://service.narvii.com/api/v1{}".format
tapjoy = "https://ads.tapdaq.com/v4/analytics/reward"


def c():
    return requests.get(f"https://pysc.cf/api/generate-did").text


def s(data):
    return requests.get(f"https://pysc.cf/api/generate-sign", params={"data": data}).text


def uu():
    return str(uuid4())
