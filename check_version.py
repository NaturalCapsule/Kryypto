import requests

from packaging import version

APP_VERSION = "1.0"
VERSION_URL = 'https://github.com/NaturalCapsule/IDE/blob/main/version/version.json'

def checkUpdate():
    # try:
    response = requests.get(VERSION_URL, timeout = 5)
    data = response.json()
    latest = data['Version']
    url = data['URL']
    if version.parse(latest) > version.parse(APP_VERSION):
        print("UPDATE KYYPTO")
    else:
        print("Up to date!")
    # except Exception as e:
        # print(e)


checkUpdate()