import requests
import time
from bs4 import BeautifulSoup as bs

# saites beigās ir "?page=1", "?page=2" utt.
URL = 'https://www.1a.lv/c/tv-audio-video-spelu-konsoles/audio-aparatura/austinas/3v2'
AUSTINAS = 'austinas/'

# saglabā lapu no url:
def saglabat(url, fails):
    rezultats = requests.get(url)
    if rezultats.status_code == 200:
        with open(f"{AUSTINAS}{fails}", 'w', encoding='UTF-8') as f:
            f.write(rezultats.text)
    else:
        print(f"ERROR: Statusa kods {rezultats.status_code}")

# saglabā vairākas lapas (cik - lapu skaits):
def lejupieladet_lapas(cik):
    for i in range(1, cik + 1):
        saglabat(f"{URL}?page={i}", f"{i}_lapa.html")
        time.sleep(1)

# iegūst austiņu saites:
def saites(cik):
    saites = []

    for i in range(1, cik + 1):

        with open(f"{AUSTINAS}{i}_lapa.html", 'r', encoding='UTF-8') as f:
            html = f.read()

            zupa = bs(html, "html.parser")

            # klase: catalog-taxons-products-container
            galvena = zupa.find("div", {"class": "catalog-taxons-products-container"})

            # klase: catalog-taxons-product catalog-taxons-product--grid-view
            sadalas = galvena.find_all("div", {"class": "catalog-taxons-product catalog-taxons-product--grid-view"})

            for sadala in sadalas:
                saite = "https://www.1a.lv"+sadala.find("a")["href"]
                saites.append(saite)

    return saites

print(saites(45))
print(len(saites(45))) # cik saites?

# pašlaik ir 45 lapas (07.10.2021.)
# lejupieladet_lapas(45)