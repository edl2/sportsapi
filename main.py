import requests
import json
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import subprocess

def get_current_date():
    return datetime.datetime.today().strftime("%Y-%m-%d")

def get_sport():
    sports = ["nba", "nfl", "mlb", "nhl", "mma", "motorsport", "cricket"]
    for i, sport in enumerate(sports):
        print(f"{i+1}. {sport.upper()}")
    selected = int(input("Which sport do you want? "))
    return sports[selected-1]

def get_inprogress_matches(sport, date):
    url = f"https://sportscentral.io/api/{sport}-tournaments?date={date}"
    response = requests.get(url)
    data = json.loads(response.text)
    return [(match["name"], match["id"]) for tournament in data for match in tournament["events"] if match["status"]["type"] == "inprogress"]

def print_match_list(matches):
    for i, (name, _) in enumerate(matches):
        print(f"{i+1}. {name}")

def get_selected_match(matches):
    selected = int(input("Which match do you want to select? "))
    name = matches[selected-1][0]
    id = matches[selected-1][1]
    return name, id

def get_channels(match_id, sport):
    url = f"https://scdn.dev/main-assets/{match_id}/{sport}?origin=sportsurge.club&="
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    channels = []
    watch_urls = []
    for tr in soup.find('tbody').find_all('tr'):
        channel = tr.find('b').text
        watch_url = tr.find('a')['href']
        channels.append(channel)
        watch_urls.append(watch_url)
    return channels, watch_urls

def print_channel_list(channels, watch_urls, scrapers):
    """Print the list of channels and their base domains, filtering out channels with a base domain not in the scrapers list"""
    from urllib.parse import urlparse
    for i, (channel, watch_url) in enumerate(zip(channels, watch_urls)):
        domain = urlparse(watch_url).netloc
        if domain in scrapers:
            print(f"{i+1}: {channel} ({domain})")



def get_selected_channel(channels, watch_urls):
    selected = int(input("Enter the number of the channel you want to watch: "))
    return watch_urls[selected-1]

date = get_current_date()
sport = get_sport()

matches = get_inprogress_matches(sport, date)

print_match_list(matches)
name, id = get_selected_match(matches)

channels, watch_urls = get_channels(id, sport)

print(f"Channels for {name}:")
scrapers = ["weakstream.org", "fabtech.work", "allsportsdaily.co", "techclips.net", "gameshdlive.xyz"]
print_channel_list(channels, watch_urls, scrapers)
url = get_selected_channel(channels, watch_urls)
site = urlparse(url).netloc
if site == "weakstream.org":
    from extracters.weakstream import *
elif site == "fabtech.work":
    from extracters.fabtech import *
elif site == "allsportsdaily.co":
    from extracters.allsportsdaily import *
elif site == "techclips.net":
    from extracters.techclips import *
elif site == "gameshdlive.xyz":
    from extracters.gameshdlive import *
m3u8 = get_link(url)
mpv = subprocess.Popen(["mpv", f"{m3u8}", f"--http-header-fields=Referer: http://{site}/"])
mpv.wait()
mpv.kill()