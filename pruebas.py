import requests
from bs4 import BeautifulSoup
import re

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

url="https://www.ascodevida.com/"

req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

def get_data(story):
    comments_num = int(story.find("a", class_="comments").get_text())
    text = story.find("a", class_="advlink").get_text()
    meta = story.find("div", class_="meta").get_text()

    [queadv, merecido, chorrada] = [int(num.strip("()")) for num in re.findall("\(\d+\)", meta)]

    return {
        "comments_num": comments_num,
        "text": text,
        "queadv": queadv,
        "merecido": merecido,
        "chorrada": chorrada
            }

stories = [get_data(story) for story in soup.find_all("div", class_="box story")]

print(stories)

