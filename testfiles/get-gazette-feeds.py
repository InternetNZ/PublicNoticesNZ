# Scrape front page of the gazette to get codes
# Download a set of dated rss files for testing code calibrations

import requests
from bs4 import BeautifulSoup
import urllib
import datetime

feed_info = {}

# Get the front page of NZ Gazette
r = requests.get("https://gazette.govt.nz")
data = r.text
soup = BeautifulSoup(data, "html.parser")

# Find the options drop-down with notice categories
options = soup.find(id="Form_NoticeSearch_noticeType").findAll('option')

for option in options[1:]:

    title = str(option.text)
    abbrev = str(option.get('value'))

    feed_info[abbrev] = title

for key in feed_info:

    url = "http://gazette.govt.nz/home/NoticeSearch?noticeType=" + key + "&rss=1"

    now = datetime.datetime.now()

    # Replace "/" characters with "-" to avoid filename complications
    filename = key + " " + feed_info[key].replace(
        "/", "-") + " " + str(now.strftime("%Y-%m-%d %H%M")) + ".txt"

    print("Downloading...")

    try:
        print("Url: " + url + " Filename: " + filename)
        urllib.urlretrieve(url, filename)
    except:
        print("Error!")


# https: // gazette.govt.nz / home / NoticeSearch?noticeType = aw & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = aa & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = al & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = ar & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = ba & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = cb & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = ct & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = fs & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = gn & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = is & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = lt & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = md & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = ot & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = pn & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = ds & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = au & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = dl & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = go & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = gs & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = ln & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = ps & rss = 1
# https: // gazette.govt.nz / home / NoticeSearch?noticeType = vr & rss = 1
