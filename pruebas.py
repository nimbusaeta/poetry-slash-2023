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

def get_data(story):
    """ Por cada box story devuelve un diccionario con los 5 datos que nos interesan.
    """
    comments_num = int(story.find("a", class_="comments").get_text())
    meta = story.find("div", class_="pre").get_text().strip()
    advlink = story.find("a", class_="advlink")
    text = advlink.get_text()
    link = advlink['href']
    votes = story.find("div", class_="meta").get_text()

    [queadv, merecido, chorrada] = [int(num.strip("()")) for num in re.findall("\(\d+\)", votes)]

    return {
        "comments_num": comments_num,
        "meta": meta,
        "text": text,
        "link": link,
        "queadv": queadv,
        "merecido": merecido,
        "chorrada": chorrada
            }


def read_page(url):
    """ Dada una url, devuelve una lista de diccionarios con todas las box stories de esa url.
    """
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser', exclude_encodings=["iso8859_10", "windows-1252", "cp850"])
    print(soup.original_encoding)

    stories = [get_data(story) for story in soup.find_all("div", class_="box story")]

    return stories[0]

def save_data(inicio, fin):
    url_base="https://www.ascodevida.com/ultimos/p/"

    all = []
    for i in range(inicio, fin):
        url = url_base + str(i)
        advs = read_page(url)
        all.append(advs)

    with open("data/pagina.txt", "w", encoding="utf-8") as f:
        f.write(str(all))

save_data(1, 2)
# Hay 8580

# character_set = [^A-ZÁÉÍÓÚáéíóúñüa-z0-9 ,.:'"{}()\[\]\\\/¿?¡!_-€@]