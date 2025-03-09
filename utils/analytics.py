# utils/analytics.py

def calculer_ratio(prix_annonce, prix_internet):
    try:
        ratio = ((prix_internet - prix_annonce) / prix_annonce) * 100
    except ZeroDivisionError:
        ratio = 0
    return round(ratio, 2)
