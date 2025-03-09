import requests
from bs4 import BeautifulSoup
import logging
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Liste de User-Agent réalistes
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }

# Création d'une session avec retries
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[403, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

def fetch_url(url):
    headers = get_random_headers()
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        time.sleep(random.uniform(2, 5))
        return response.text
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de {url}: {e}")
        return ""

def scraper_leboncoin(url):
    html = fetch_url(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    annonces = []
    for item in soup.find_all("div", class_="item"):
        titre_tag = item.find("h2")
        prix_tag = item.find("span", class_="price")
        if titre_tag and prix_tag:
            titre = titre_tag.get_text(strip=True)
            prix_str = prix_tag.get_text(strip=True)
            prix_annonce = int("".join(filter(str.isdigit, prix_str)) or 0)
            prix_internet = int(prix_annonce * 1.2)
            demande = 8
            annonces.append({
                "titre": titre,
                "prix_annonce": prix_annonce,
                "prix_internet": prix_internet,
                "demande": demande
            })
    return annonces
