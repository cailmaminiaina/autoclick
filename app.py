import requests
import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# URL cible
url = "https://getallmylinks.com/jesscute1"

# Fonction pour récupérer une liste de proxies gratuits
def get_free_proxies():
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    proxies = []
    for row in soup.select("table tbody tr"):
        ip = row.select_one("td").text
        port = row.select("td")[1].text
        proxies.append(f"http://{ip}:{port}")

    return proxies

# Récupérer les proxies
proxies_list = get_free_proxies()
print(f"Proxies récupérés : {len(proxies_list)}")

# Générateur de User-Agent aléatoire
ua = UserAgent()

# Effectuer 500 requêtes
for i in range(500):
    if not proxies_list:
        print("Plus de proxies disponibles, récupération de nouveaux proxies...")
        proxies_list = get_free_proxies()

    proxy = random.choice(proxies_list)  # Sélection aléatoire d'un proxy
    headers = {"User-Agent": ua.random}  # User-Agent aléatoire

    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=10)

        if response.status_code == 200:
            print(f"[{i+1}/500] Click via {proxy} - Status: {response.status_code}")
        else:
            print(f"[{i+1}/500] Erreur HTTP {response.status_code} via {proxy}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur avec {proxy}: {e}")
        proxies_list.remove(proxy)  # Supprime le proxy défectueux

    # Pause aléatoire pour éviter d’être détecté comme un bot
    time.sleep(random.uniform(1, 5))
