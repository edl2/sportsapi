import re
import requests
import subprocess
from bs4 import BeautifulSoup
import json
def get_link(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    iframe = soup.iframe
    src = iframe['src']
    r_src = requests.get(src).text
    fid = re.findall(r"t>fid='(.*?)'", r_src)[0]
    n = re.findall(r"embed(.*?).j", r_src)[0]
    php = f"https://vikistream.com/embed{n}.php?player=desktop&live={fid}"
    r_php = requests.get(php).text
    expand = re.findall(r"n\((.*?).join", r_php)[0]
    lis = json.loads(expand)
    m3u8 = "".join(lis)
    return m3u8

site = "vikistream.com"






# Find the script tag that contains the fid and src values

# Extract the fid value
#print(fid)  # Output: 'do32'

# Extract the src value
#print(src)  # Output: '//vikistream.com/embed2.js'
