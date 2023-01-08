import requests
import re
url = "https://gameshdlive.xyz/zab/ch11.php"
def get_link(url):
    r = requests.get(url).text
    php = re.findall(r"s' src='(.*?)'", r)[0]
    r_php = requests.get(php).text
    m3u8 = re.findall(r"source: '(.*?)'", r_php)[0]
    return m3u8
print(get_link(url))
