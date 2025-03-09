# agents/agent_leboncoin.py

from agents.agent_base import AgentBase
from scrapers.scraper_leboncoin import scraper_leboncoin

class AgentLeBonCoin(AgentBase):
    def __init__(self, config):
        super().__init__(categorie="smartphones", config=config)

    def collecter_donnees(self):
        url = "https://www.leboncoin.fr/recherche?category=smartphones"
        annonces = scraper_leboncoin(url)
        self.results = annonces
