# agents/agent_base.py

import os
from datetime import datetime
from utils.analytics import calculer_ratio
import logging

class AgentBase:
    def __init__(self, categorie, config):
        self.categorie = categorie
        self.config = config
        self.results = []

    def collecter_donnees(self):
        raise NotImplementedError("Implémentez collecter_donnees() dans l'agent.")

    def analyser(self):
        for annonce in self.results:
            ratio = calculer_ratio(annonce['prix_annonce'], annonce['prix_internet'])
            annonce['profit_ratio'] = ratio
        self.results = sorted(self.results, key=lambda x: x['profit_ratio'], reverse=True)

    def generer_rapport(self):
        import pandas as pd
        df = pd.DataFrame(self.results)
        dossier = self.config['REPORT_FOLDER']
        os.makedirs(dossier, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"{dossier}/rapport_{self.categorie}_{timestamp}.csv"
        df.to_csv(nom_fichier, index=False)
        logging.info(f"Rapport généré : {nom_fichier}")
        return nom_fichier

    def executer(self):
        self.collecter_donnees()
        self.analyser()
        return self.generer_rapport()
