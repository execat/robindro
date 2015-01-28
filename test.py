import requests
import sqlite3
import time
import string
from urllib.parse import urljoin
import code
from bs4 import BeautifulSoup

errors = []

# Helper functions
def prepare():
    # Create database, table and index
    conn = sqlite3.connect("geetabitan.db")
    c = conn.cursor()
    create_string = '''
        CREATE TABLE IF NOT EXISTS geetabitan_links
        (
            song_name string, song_link string,
            translation_available integer,
            created_at numeric, updated_at numeric,
            lyric text, english_lyric text, notes text,
            english_translation text,
            notation_url string, notation_path string,
            pdf_url string, pdf_path string,
            midi_url string, midi_path string,
            listen_url string, listen_path string
        )
    '''
    c.execute(create_string)
    index_string = "CREATE UNIQUE INDEX IF NOT EXISTS UniqueSongLinks ON geetabitan_links (song_link)"
    c.execute(index_string)
    conn.commit()
    conn.close()

def request(url):
    source_code = requests.get(url)
    plain_text = source_code.content
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

def song_list_spider(song_list_urls):
    for song_list_index, url in song_list_urls.items():
        soup = request(url)
        song_urls = {}
        for link in soup.select(".lyricsname > div > ul > li > a"):
            base_url = urljoin("http://www.geetabitan.com/lyrics/", song_list_index + '/')
            page_name = link.get_text()
            page_link = urljoin(base_url, link.get('href'))
            song_urls[page_name] = page_link
        song_spider(song_urls)

def song_spider(song_urls):
    insert_array = []
    for song_name, url in song_urls.items():
        soup = request(url)
        for content in soup.select(".songmatter"):
            try:
                song_link = url
                lyric = extract_lyric(content)
                notes = extract_notes(content)
                notation_url = extract_notation_url(content, url)
                pdf_url, midi_url = extract_staff(content, url)
                english_lyric = extract_english_lyric(content)
                english_translation = extract_english_trans(content)
                listen_url = extract_listen(content, url)
                print(song_name, song_link)
                insert_array.append((song_name, song_link, lyric, notes, notation_url, pdf_url, midi_url, english_lyric, english_translation, listen_url, time.time()))
            except Exception as e:
                errors.append([song_name, song_url, 'song_spider', e])
    push_array(insert_array)


def push_array(insert_array):
    conn = sqlite3.connect("geetabitan.db")
    c = conn.cursor()
    try:
        c.executemany("INSERT INTO geetabitan_links (song_name, song_link, lyric, notes, notation_url, pdf_url, midi_url, english_lyric, english_translation, listen_url, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_array)
    except sqlite3.OperationalError as exception:
        errors.append([song_name, song_url, 'song_spider', e])
    finally:
        conn.commit()
        conn.close()

def push_song(song_name, song_link, lyric, notes, notation_url, pdf_url, midi_url, english_lyric, english_translation, listen_url):
    conn = sqlite3.connect("geetabitan.db")
    c = conn.cursor()
    insert_array = [(song_name, song_link, lyric, notes, notation_url, pdf_url, midi_url, english_lyric, english_translation, listen_url, time.time())]
    try:
        c.executemany("INSERT INTO geetabitan_links (song_name, song_link, lyric, notes, notation_url, pdf_url, midi_url, english_lyric, english_translation, listen_url, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_array)
    except sqlite3.OperationalError as exception:
        errors.append([song_name, song_url, 'song_spider', e])
    finally:
        conn.commit()
        conn.close()

# Extractor methods
def extract_lyric(content):
    try:
        return content.find(id="faq1").find("pre").get_text()
    except AttributeError:
        errors.append([song_name, song_url, 'extract_lyric', e])
        return None

def extract_notes(content):
    try:
        return content.find(id="faq2").get_text()
    except:
        errors.append([song_name, song_url, 'extract_notes', e])
        return None

def extract_notation_url(content, url):
    a = content.find(id="faq3")
    try:
        if a.get_text().find("Notation not available.") > -1:
            return None
        return urljoin(url, a.find("p").find("img").get("src"))
    except AttributeError:
        errors.append([song_name, song_url, 'extract_notation', e])
        return None

def extract_staff(content, url):
    try:
        links = content.find(id="faq4").find_all("a")
        pdf_link = midi_link = ""
        for link in links:
            if link.get("href").find('pdf/') == 0:
                pdf_link_rel = link.get("href")
                pdf_link = urljoin(url, pdf_link_rel)
            if link.get("href").find('midi/') == 0:
                midi_link_rel = link.get("href")
                midi_link = urljoin(url, midi_link_rel)
        return (pdf_link, midi_link)
    except AttributeError:
        errors.append([song_name, song_url, 'extract_staff', e])
        return None

def extract_english_lyric(content):
    try:
        return content.find("div", id="faq5").find("pre").get_text()
    except AttributeError:
        errors.append([song_name, song_url, 'extract_english_lyric', e])
        return None

def extract_english_trans(content):
    try:
        string_value = content.find(id="faq6").find("pre").get_text()
        if string_value.find("Will be available soon but if someone requires it please contact.") < 0:
            return string_value
    except AttributeError:
        errors.append([song_name, song_url, 'extract_english_trans', e])
        return None

def extract_listen(content, url):
    try:
        link = content.find(id="faq7").find("a").get("href")
        if link.find("sendyoursong.html") > -1:
            return None
        return urljoin(url, link)
    except AttributeError:
        errors.append([song_name, song_url, 'extract_listen', e])
        return None

# Process
prepare()

index_spider()
# For testing a song list:
# song_list_spider({'U': 'http://www.geetabitan.com/lyrics/U/song-list.html'})
# For testing a song page:
# song_spider({'Shunyo Pran Kaade Soda': 'http://www.geetabitan.com/lyrics/S/shunyo-pran-kaade-soda.html'})

# Error reporting
print(errors)
code.interact(local=locals())
