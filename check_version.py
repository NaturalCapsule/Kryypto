import requests

from packaging import version

APP_VERSION = "1.0.1"
VERSION_URL = "https://raw.githubusercontent.com/NaturalCapsule/IDE/main/version/version.json"

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
        print(e)