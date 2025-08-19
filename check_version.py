import requests

from packaging import version

APP_VERSION = "1.0.0"
VERSION_URL = "https://raw.githubusercontent.com/NaturalCapsule/IDE/main/version/version.json"

def checkUpdate():
    try:
        response = requests.get(VERSION_URL, timeout = 5)
        data = response.json()
        latest = data['Version']
        url = data['URL']
        if version.parse(latest) > version.parse(APP_VERSION):
            # print("UPDATE KYYPTO")
            return url
        else:
            # print("Up to date!")
            return None
    except Exception as e:
        print(e)


checkUpdate()