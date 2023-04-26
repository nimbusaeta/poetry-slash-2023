import requests
from bs4 import BeautifulSoup
import re
import csv

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
    undesired_encodings = [
        "iso-8859-2", "iso-8859-5",
        "iso8859_4", "iso8859_9", "iso8859_10", "iso8859_11", "iso8859_13", "iso8859_14", "iso8859_15", "iso8859_16",
        "windows-1252", "windows-1250",
        "cp775", "cp850", "cp852", "cp864", "cp932", "ptcp154", "cp1125",
        "hp_roman8", "mac_iceland", "koi8-r", "mac_latin2"
        ]

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser', exclude_encodings=undesired_encodings)
    
    if soup.original_encoding != "utf-8":
        print(soup.original_encoding)

    stories = [get_data(story) for story in soup.find_all("div", class_="box story")]

    return stories

def save_data(inicio, fin):
    url_base="https://www.ascodevida.com/ultimos/p/"

    for i in range(inicio, fin):
        #print(i)
        url = url_base + str(i)
        advs = read_page(url)

        with open("data/pagina.csv", "a", newline='', encoding="utf-8") as f:
            fieldnames = ['comments_num', 'meta', 'text', 'link', 'queadv', 'merecido', 'chorrada']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for adv in advs:
                writer.writerow(adv)

save_data(8000, 8591) # descargado el 6 de abril de 2023
# Hay 8590

# character_set = [^A-ZÁÉÍÓÚÀÈÌÒÙÑÄËÏÖÜÇa-záéíóúàèìòùñäëïöüç0-9 ,‚.:;·'‛‘’´"“”«»`´^<>{}()\[\]\\\/¿?¡!_|\-–€$£&%@#♂♀ºª°²*+=…¬~]
# regex fecha = \d+ \w{3} \d{4}, \d\d:\d\d