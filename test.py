import requests
import sqlite3
import time
import string
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

def index_spider():
    base_url = "http://www.geetabitan.com/lyrics/"
    url = base_url + "/index.html"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    code.interact(local=locals())
    subpage = soup.find("div", class_="alphabet")
    song_list_urls = []
    for link in subpage.find_all("a"):
        page_link = base_url + "/" + link.get('href')
        song_list_urls.append(page_link)
    song_list_spider(song_list_urls)

def song_list_spider(urls):
    print()

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
