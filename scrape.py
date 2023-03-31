import requests
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def get_advs(url):
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    advs = [link.get_text() for link in soup.find_all("a", class_="advlink")]

    return advs

url_base="https://www.ascodevida.com/ultimos/p/"

for i in range(1, 8581):
    url = url_base + str(i)
    advs = get_advs(url)
    print(str(i), advs[0])



'''
with open("pagina.txt", "w", encoding="utf-8") as f:
    f.write(page)
    '''