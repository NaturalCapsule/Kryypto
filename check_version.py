import requests

from packaging import version

APP_VERSION = "1.6.0"
VERSION_URL = "https://raw.githubusercontent.com/NaturalCapsule/Kryypto/main/version/version.json"

def checkUpdate():
    try:
        response = requests.get(VERSION_URL, timeout = 5)
        data = response.json()
        latest = data['Version']
        url = data['URL']
        if version.parse(latest) > version.parse(APP_VERSION):
            return url
        else:
            return None
    except Exception as e:
        # print(e)
        return "Error: "+str(e)