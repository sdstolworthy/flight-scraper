import requests

def OpenURL(url):
    r = requests.get(url)
    feed = str(r.content)
