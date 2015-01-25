import requests
from bs4 import BeautifulSoup

def song_list_spider(letters):
    letter = letters[0]
    while page < len(letters):
        url = "http://www.geetabitan.com/lyrics/" + str(letter) + "/song-list.html"



"""
http://www.geetabitan.com/lyrics/index.html
http://www.geetabitan.com/lyrics/A/song-list.html
http://www.geetabitan.com/lyrics/eng-trans-A.html
"""
