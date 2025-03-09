# utils/predictor.py

import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def entrainer_modele(data_csv, model_file):
    df = pd.read_csv(data_csv)
    X = df[['prix_annonce', 'prix_internet', 'demande']]
    y = df['profit_ratio']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Erreur quadratique moyenne : {mse}")
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
    print(f"Modèle entraîné et sauvegardé dans {model_file}")
    return model

def charger_modele(model_file):
    if os.path.exists(model_file):
        with open(model_file, "rb") as f:
            model = pickle.load(f)
        return model
    else:
        print("Modèle non trouvé. Veuillez entraîner le modèle d'abord.")
        return None

def predire_profit_ratio(prix_annonce, prix_internet, demande, model):
    X = [[prix_annonce, prix_internet, demande]]
    prediction = model.predict(X)
    return round(float(prediction[0]), 2)
