import requests
import re
import random
from urllib.parse import urlparse, quote
import base64

def get_link(url):
    r = requests.get(url).text
    path = urlparse(url).path.split("/")[-1]
    math = str(round(random.random() * 64))
    r = requests.get(f"http://1stream.eu/getspurcename?{path}={math}").text
    r2 = re.findall(r":\"(.*?)\"", r)[0]
    m3u8 = base64.b64decode(r2).decode("utf-8")
    return m3u8