import pandas as pd

# Chemin vers votre fichier CSV
csv_file_path = 'app/data/dataFinale.csv'


# Fonction pour préparer les données pour l'affichage
def prepare_dropdown_data():
    # Lecture du fichier CSV
    df = pd.read_csv(csv_file_path)

    # Conversion de la colonne 'Date' en datetime si elle n'est pas déjà
    df['date'] = pd.to_datetime(df['date'])

    # Extraction des valeurs uniques pour chaque colonne
    # unique_boutiques = df['boutique'].unique().tolist()
    unique_canals = df['canal'].unique().tolist()
    unique_stores = df['store'].unique().tolist()
    unique_dates = df['date'].dt.strftime('%Y-%m-%d').unique().tolist()  # Formatage si nécessaire
    unique_categories = df['categorie'].unique().tolist()
    unique_souscats = df['sousCat'].unique().tolist()
    unique_noms_articles = df['nomArticle'].unique().tolist()
    unique_new_rework = df['new-Rework'].unique().tolist()
    #   unique_quantites = df['Quantite'].unique().tolist()
    #   unique_instock = df['Instock'].unique().tolist()
    #   unique_delivres = df['Delivre'].unique().tolist()

    # Préparation des données pour l'affichage
    dropdown_data = {
        "canal": [{"name": canal} for canal in unique_canals],
        "store": [{"name": store} for store in unique_stores],
        "date": [{"name": date} for date in unique_dates],
        "categorie": [{"name": categorie} for categorie in unique_categories],
        "sousCat": [{"name": souscat} for souscat in unique_souscats],
        "nomArticle": [{"name": nom_article} for nom_article in unique_noms_articles],
        "new-Rework": [{"name": new_rework} for new_rework in unique_new_rework],
        # "Quantite": [{"name": quantite} for quantite in unique_quantites],
        # "Instock": [{"name": instock} for instock in unique_instock],
        # "Delivre": [{"name": delivre} for delivre in unique_delivres]
    }

    return dropdown_data


"""
def prepare_dropdown_data2(canal_filter=None, category_filter=None, subcategory_filter=None):
    df = pd.read_csv(csv_file_path)
    df['date'] = pd.to_datetime(df['date'])

    if category_filter:
        df = df[df['categorie'] == category_filter]

    if subcategory_filter:
        df = df[df['sousCat'] == subcategory_filter]

    unique_canals = df['canal'].unique().tolist()
    unique_stores = df['store'].unique().tolist()
    unique_dates = df['date'].dt.strftime('%Y-%m-%d').unique().tolist()
    unique_categories = df['categorie'].unique().tolist()
    unique_souscats = df['sousCat'].unique().tolist()
    unique_noms_articles = df['nomArticle'].unique().tolist()
    unique_new_rework = df['new-Rework'].unique().tolist()

    dropdown_data = {
        "canal": [{"name": canal} for canal in unique_canals],
        "store": [{"name": store} for store in unique_stores],
        "date": [{"name": date} for date in unique_dates],
        "categorie": [{"name": categorie} for categorie in unique_categories],
        "sousCat": [{"name": souscat} for souscat in unique_souscats],
        "nomArticle": [{"name": nom_article} for nom_article in unique_noms_articles],
        "new-Rework": [{"name": new_rework} for new_rework in unique_new_rework],
    }

    return dropdown_data
"""