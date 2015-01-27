import requests
import sqlite3
from bs4 import BeautifulSoup

def song_list_spider(letters):
    conn = sqlite3.connect("testing.db")

    letter = letters[0]
    while page < len(letters):
        base_url = "http://www.geetabitan.com/lyrics/" + str(letter)
        url = base_url + "/song-list.html"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)

        subpage = soup.find("div", class_="lyricsname")
        for link in subpage.find_all("a"):
            page_name = link.get_text()
            page_link = base_url + "/" + link.get('href')




"""
http://www.geetabitan.com/lyrics/index.html
http://www.geetabitan.com/lyrics/A/song-list.html
http://www.geetabitan.com/lyrics/eng-trans-A.html
"""
