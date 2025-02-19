import requests
import random
import time
from datetime import datetime, timedelta
from fake_useragent import UserAgent

# URL cible
url = "https://getallmylinks.com/jesscute1"

# Configuration des proxies Bright Data
BRIGHT_DATA_HOST = "brd.superproxy.io"
BRIGHT_DATA_PORT = "33335"
BRIGHT_DATA_USERNAME = "brd-customer-hl_048c6da0-zone-residential_proxy1"
BRIGHT_DATA_PASSWORD = "drfox4y86uww"  # 🔴
ssl_path = "BrightData SSL certificate (port 33335).crt"

# Liste de pays (modifier selon les besoins)
COUNTRIES = ["us", "us", "us", "us", "us", "gb", "ca", "au", "nz", "fr"]

# Générateur de User-Agent aléatoire
ua = UserAgent()

# Nombre maximum de clics par jour
MAX_CLICKS_PER_DAY = 500
clicks_today = 0

# Enregistrer l'heure de début pour suivre les clics quotidiens
start_time = datetime.now()

while True:
    # Vérifier si on a atteint 400 clics aujourd'hui
    current_time = datetime.now()
    if (current_time - start_time).days >= 1:
        # Réinitialiser le compteur tous les jours
        start_time = datetime.now()
        clicks_today = 0

    if clicks_today >= MAX_CLICKS_PER_DAY:
        # Attendre jusqu'à minuit pour recommencer
        print("🎯 Objectif atteint : 400 clics aujourd'hui. Pause jusqu'à demain...")
        time_to_midnight = (datetime.now().replace(hour=23, minute=59, second=59) - datetime.now()).seconds
        time.sleep(time_to_midnight + 1)  # Attendre jusqu'à minuit
        clicks_today = 0  # Réinitialiser le compteur

    # Sélectionner un pays aléatoire pour le proxy
    country = random.choice(COUNTRIES)

    # Construire le proxy avec authentification Bright Data
    proxy_auth = f"http://{BRIGHT_DATA_USERNAME}-country-{country}:{BRIGHT_DATA_PASSWORD}@{BRIGHT_DATA_HOST}:{BRIGHT_DATA_PORT}"
    proxies = {"http": proxy_auth, "https": proxy_auth}

    headers = {"User-Agent": ua.random}  # User-Agent aléatoire

    try:
        response = requests.get(url, proxies=proxies, headers=headers, timeout=10, verify=ssl_path)

        if response.status_code == 200:
            print(f"[{clicks_today + 1}/{MAX_CLICKS_PER_DAY}] ✅ Click via {country.upper()} - Status: {response.status_code}")
        else:
            print(f"[{clicks_today + 1}/{MAX_CLICKS_PER_DAY}] ❌ Erreur HTTP {response.status_code} via {country.upper()}")

        clicks_today += 1  # Incrémenter le compteur

    except requests.exceptions.RequestException as e:
        print(f"[{clicks_today + 1}/{MAX_CLICKS_PER_DAY}] ⚠️ Erreur avec proxy {country.upper()}")

    # Pause aléatoire entre 30 et 600 secondes (0.5 à 10 minutes)
    sleep_time = random.uniform(30, 600)
    print(f"⏳ Pause de {sleep_time:.2f} secondes avant le prochain clic...")
    time.sleep(sleep_time)