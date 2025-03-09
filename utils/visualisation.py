# utils/visualisation.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def generer_graphique(df, categorie, output_folder):
    plt.figure(figsize=(10, 6))
    df.plot(kind="bar", x="titre", y="profit_ratio", legend=False)
    plt.xlabel("Annonce")
    plt.ylabel("Profit Ratio (%)")
    plt.title(f"Profit Ratio par annonce - {categorie}")
    plt.tight_layout()
    os.makedirs(output_folder, exist_ok=True)
    image_path = os.path.join(output_folder, f"graph_{categorie}.png")
    plt.savefig(image_path)
    plt.close()
    return image_path

def generer_tableau_comparatif(df, output_folder, categorie):
    os.makedirs(output_folder, exist_ok=True)
    table_html = df.to_html(index=False, classes="table")
    html_path = os.path.join(output_folder, f"tableau_{categorie}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(table_html)
    return html_path
