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
        song_spider(song_urls)

def song_spider(song_urls):
    for url in song_urls:
        soup = request(url)
        for content in soup.select(".songmatter"):
            lyric = extract_lyric(content)
            notes = extract_notes(content)
            notation_url = extract_notation_url(content, url)
            pdf_link, midi_link = extract_staff(content, url)
            english_lyric = extract_english_lyric(content)
            english_trans = extract_english_trans(content)
            listen = extract_listen(content, url)
            push_song(lyric, notes, notation, staff, english_lyric, english_trans, listen)

def push_song(lyric, notes, notation, staff, english_lyric, english_trans, listen):
    pass

# Extractor methods
def extract_lyric(content):
    return content.find(id="faq1").find("pre").get_text()

def extract_notes(content):
    return content.find(id="faq2").get_text()

def extract_notation_url(content, url):
    a = content.find(id="faq3")
    if a.get_text().find("Notation not available.") > -1:
        return None
    try:
        return urljoin(url, a.find("p").find("img").get("src"))
    except AttributeError:
        return None

def extract_staff(content, url):
    links = content.find(id="faq4").find_all("a")
    pdf_link = midi_link = ""
    for link in links:
        if link.get("href").find('pdf/') == 0:
            pdf_link_rel = link.get("href")
            pdf_link = urljoin(url, pdf_link_rel)
        if link.get("href").find('midi/') == 0:
            midi_link_rel = link.get("href")
            midi_link = urljoin(url, midi_link_rel)
    code.interact(local=locals())
    return (pdf_link, midi_link)

def extract_english_lyric(content):
    return content.find("div", id="faq5").find("pre").get_text()

def extract_english_trans(content):
    string_value = content.find(id="faq6").find("pre").get_text()
    if string_value.find("Will be available soon but if someone requires it please contact.") < 0:
        return string_value
    return None

def extract_listen(content, url):
    link = content.find(id="faq7").find("a").get("href")
    if link.find("sendyoursong.html") > -1:
        return None
    return urljoin(url, link)

# code.interact(local=locals())

# Initialize
conn = sqlite3.connect("geetabitan.db")
c = conn.cursor()

# Process
prepare()
index_spider()

# Destroy
conn.commit()
conn.close()
