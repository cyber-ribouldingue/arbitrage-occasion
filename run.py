# run.py

import os
import pandas as pd
from agents.agent_leboncoin import AgentLeBonCoin
from config import REPORT_FOLDER, IA_MODEL_FILE
from utils.visualisation import generer_graphique, generer_tableau_comparatif
from utils.predictor import charger_modele, predire_profit_ratio

def main():
    config = {"REPORT_FOLDER": REPORT_FOLDER, "MIN_PROFIT_RATIO": 15}

    # Ici, nous utiliserons un agent pour Le Bon Coin par exemple
    agent = AgentLeBonCoin(config)

    print(f"Exécution de l'agent pour la catégorie : {agent.categorie}")
    rapport_csv = agent.executer()

    # Vérifier que le fichier n'est pas vide
    if not os.path.exists(rapport_csv) or os.path.getsize(rapport_csv) == 0:
        print(f"Aucun rapport généré pour la catégorie {agent.categorie} (fichier vide).")
        return

    try:
        df = pd.read_csv(rapport_csv)
    except pd.errors.EmptyDataError:
        print(f"Le fichier {rapport_csv} est vide. Passage à la suite.")
        return

    # Si le modèle est entraîné, appliquer des prédictions
    modele = charger_modele(IA_MODEL_FILE)
    if modele:
        df['profit_ratio_ia'] = df.apply(
            lambda row: predire_profit_ratio(row['prix_annonce'], row['prix_internet'], row['demande'], modele),
            axis=1
        )
        df['profit_ratio_final'] = (df['profit_ratio'] + df['profit_ratio_ia']) / 2

    os.makedirs(REPORT_FOLDER, exist_ok=True)
    rapport_destination = os.path.join(REPORT_FOLDER, f"rapport_{agent.categorie}.csv")
    df.to_csv(rapport_destination, index=False)
    print(f"Rapport copié dans {rapport_destination}")

    graph_path = generer_graphique(df, agent.categorie, REPORT_FOLDER)
    tableau_path = generer_tableau_comparatif(df, REPORT_FOLDER, agent.categorie)
    print(f"Graphique généré : {graph_path}")
    print(f"Tableau généré : {tableau_path}")

if __name__ == "__main__":
    main()
