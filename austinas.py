import requests
import time
from bs4 import BeautifulSoup as bs

# saites beigās ir "?page=1", "?page=2" utt.
URL = 'https://www.1a.lv/c/tv-audio-video-spelu-konsoles/audio-aparatura/austinas/3v2'
AUSTINAS = 'austinas/'
TEMP = 'temp/'

# saglabā lapu no url:
def saglabat(url, cels, fails):
    rezultats = requests.get(url)
    if rezultats.status_code == 200:
        with open(f"{cels}{fails}", 'w', encoding='UTF-8') as f:
            f.write(rezultats.text)
    else:
        print(f"ERROR: Statusa kods {rezultats.status_code}")

# saglabā vairākas lapas (cik - lapu skaits):
def lejupieladet_lapas(cik, cels):
    for i in range(1, cik + 1):
        saglabat(f"{URL}?page={i}", cels, f"{i}_lapa.html")
        # time.sleep(1)

# iegūst austiņu saites:
def saites(cik, cels):
    saites = []

    for i in range(1, cik + 1):

        with open(f"{cels}{i}_lapa.html", 'r', encoding='UTF-8') as f:
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

# info par vienām austiņām:
def info(cels, fails):
    info = {}
    with open(f"{cels}{fails}", 'r', encoding='UTF-8') as f:
        html = f.read()

    zupa = bs(html, "html.parser")

    # klase: product-righter google-rich-snippet
    galvena1 = zupa.find("div", {"class": "product-righter google-rich-snippet"})

    info['produkta_nosaukums'] = galvena1.find("h1").text.replace('\n', '')
    info['produkta_kods'] = galvena1.find("p").text.replace('\n', '').replace("Preces kods: ", '')
    info['cena'] = galvena1.find("span", {"class": "price"}).find("span").text.replace(',','.')


    # # klase: products-panel__body universal-panel__body
    # galvena2 = zupa.find("div", {"class": "products-panel__body universal-panel__body"})

    # # 2 tabulas:
    # tabulas = galvena2.find_all("table")

    # tabula = tabulas[0].find("a")

    # return tabula[0]

    # tabulas[1]

    return info


# pašlaik ir 45 lapas (07.10.2021.)
# cik = 45
# lejupieladet_lapas(cik, TEMP)

# saites = saites(45, TEMP)
# cik = len(saites) # cik saites?

# for i in range(1, cik):
#     saglabat(saites[i], AUSTINAS, f"{i}_lapa.html")

print(info(AUSTINAS, "1_lapa.html"))