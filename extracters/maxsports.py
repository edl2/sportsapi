import requests
import re
import subprocess

url = "http://maxsports.site/fb-epl/"
def get_link(url):
    r = requests.get(url).text
    re = re.find()
m3u8 = "http://185.53.89.183/hls/M1.m3u8"
site = "maxsports.site"
mpv = subprocess.Popen(["mpv", f"{m3u8}", f"--http-header-fields=Referer: http://{site}/"])
mpv.wait()
mpv.kill()