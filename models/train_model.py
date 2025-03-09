# train_model.py

import os
from utils.predictor import entrainer_modele
from config import IA_MODEL_FILE

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_csv = os.path.join(current_dir, "..", "data", "historique.csv")
    model = entrainer_modele(data_csv, IA_MODEL_FILE)
