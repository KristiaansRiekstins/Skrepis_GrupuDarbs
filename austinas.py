import requests
import time

# saites beigās ir "?page=1", "?page=2" utt.
URL = 'https://www.1a.lv/c/tv-audio-video-spelu-konsoles/audio-aparatura/austinas/3v2'
AUSTINAS = 'austinas/'

def saglabat(url, fails):
    rezultats = requests.get(url)
    if rezultats.status_code == 200:
        with open(f"{AUSTINAS}{fails}", 'w', encoding='UTF-8') as f:
            f.write(rezultats.text)
    else:
        print(f"ERROR: Statusa kods {rezultats.status_code}")

def lejupieladet_lapas(cik):
    for i in range(1, cik + 1):
        saglabat(f"{URL}?page={i}", f"{i}_lapa.html")
        time.sleep(1)



# pašlaik ir 45 lapas (07.10.2021.)
lejupieladet_lapas(45)