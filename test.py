import requests
import sqlite3
import time
import string
from urllib.parse import urljoin
import code
from bs4 import BeautifulSoup

# Helper functions
def prepare():
    # Create database, table and index
    create_string = '''
        CREATE TABLE IF NOT EXISTS geetabitan_links
        (
            song_name string, song_link string,
            translation_available integer,
            created_at integer, updated_at integer,
            lyric text, english_lyric text, notes text, notation text,
            staff_notation text, english_translation text
        )
    '''
    c.execute(create_string)
    index_string = "CREATE UNIQUE INDEX IF NOT EXISTS UniqueSongLinks ON geetabitan_links (song_link)"
    c.execute(index_string)

def request(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    return BeautifulSoup(plain_text)

def index_spider():
    base_url = "http://www.geetabitan.com/lyrics/"
    url = urljoin(base_url, "index.html")
    soup = request(url)

    song_list_urls = {}
    for link in soup.select(".alphabet > ul > li > a"):
        page_name = link.get_text()
        page_link = urljoin(base_url, link.get('href'))
        song_list_urls[page_name] = page_link
    song_list_spider(song_list_urls)

def song_list_spider(urls):
    for index, url in urls.items():
        soup = request(url)
        song_urls = []
        for link in soup.select(".lyricsname > div > ul > li > a"):
            base_url = urljoin("http://www.geetabitan.com/lyrics/", index + '/')
            page_link = urljoin(base_url, link.get('href'))
            song_urls.append(page_link)
        print(song_urls)
        # song_spider(song_urls)




# Initialize
conn = sqlite3.connect("geetabitan.db")
c = conn.cursor()

# Process
prepare()
index_spider()

# Destroy
conn.commit()
conn.close()

"""
http://www.geetabitan.com/lyrics/index.html
http://www.geetabitan.com/lyrics/A/song-list.html
http://www.geetabitan.com/lyrics/eng-trans-A.html
"""
