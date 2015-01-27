import requests
import sqlite3
import time
import string
from bs4 import BeautifulSoup

def song_list_spider(letters):
    # Create database and table
    conn = sqlite3.connect("geetabitan.db")
    c = conn.cursor()
    create_string = '''
            CREATE TABLE geetabitan_links
            (song_name string, song_link string, created_at datetime)
    '''
    c.execute(create_string)

    for letter in letters:
        base_url = "http://www.geetabitan.com/lyrics/" + str(letter)
        url = base_url + "/song-list.html"
        source_code = requests.get(url)
        if source_code.status_code != 200:
            continue
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)

        subpage = soup.find("div", class_="lyricsname")
        for link in subpage.find_all("a"):
            page_name = link.get_text()
            page_link = base_url + "/" + link.get('href')
            insert_string = '''
                    INSERT INTO geetabitan_links VALUES
                    ('%s', '%s', %s)
            ''' %(page_name, page_link, time.time())
            print(insert_string)
            c.execute(insert_string)
    conn.commit()
    conn.close()

song_list_spider(list(string.ascii_uppercase))


"""
http://www.geetabitan.com/lyrics/index.html
http://www.geetabitan.com/lyrics/A/song-list.html
http://www.geetabitan.com/lyrics/eng-trans-A.html
"""
