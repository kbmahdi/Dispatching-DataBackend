import math

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict

# Path to your CSV file
csv_file_path = 'app/data/dataFinale.csv'


# -------------------Etat Stock et vente-------------------

def read_csv_to_list():
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries
    data_list = df.to_dict('records')

    return data_list


def dateDataframe(csv_file):
    """
    Calculates the minimum and maximum dates from a CSV file and returns them.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing the minimum and maximum dates.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract the date column and convert it to datetime
    date_column = pd.to_datetime(df['date'])

    # Calculate the minimum and maximum dates
    min_date = date_column.min()
    max_date = date_column.max()

    return min_date, max_date


def parse_date_range(date_range_str):
    today = datetime.now()
    if date_range_str == "All time":
        # Return a tuple that represents the entire date range, effectively returning all data
        return None, None
    elif date_range_str == "Last week":
        return today - timedelta(days=6), today
    elif date_range_str == "Last 10 days":
        return today - timedelta(days=9), today
    elif date_range_str == "Last 15 days":
        return today - timedelta(days=14), today
    elif date_range_str == "Last 30 days":
        return today - timedelta(days=29), today
    elif date_range_str == "Last 60 days":
        return today - timedelta(days=59), today
    elif date_range_str == "Last 90 days":
        return today - timedelta(days=89), today
    elif date_range_str == "Last 6 months":
        return today - timedelta(days=179), today
    else:
        raise ValueError(f"Unknown date range: {date_range_str}")


def count_non_sunday_days(date_range_str):
    start_date, end_date = parse_date_range(date_range_str)
    print(start_date, end_date)

    if start_date is None or end_date is None:
        start_date, end_date = dateDataframe(csv_file_path)

    current_date = start_date
    non_sunday_count = 0

    while current_date <= end_date:
        if current_date.weekday() != 6:  # 6 represents Sunday
            non_sunday_count += 1
        print(current_date, current_date.weekday())
        current_date += timedelta(days=1)

    return non_sunday_count


def calculate_metrics(csv_file_path, date_range_str=""):
    start_date, end_date = parse_date_range(date_range_str)
    df = pd.read_csv(csv_file_path)

    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Skip filtering if start_date and end_date are None
    if start_date is None and end_date is None:
        filtered_df = df.copy()
        # Use the full date range of the data for counting weekdays
        start_date = df['date'].min()
        end_date = df['date'].max()
    else:
        # Now perform the filtering
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Calculate the number of non-Sunday days within the specified date range
    weekdays_count = count_non_sunday_days(date_range_str)

    # instock: la somme des produits qui sont instock
    total_instock = float(filtered_df['instock'].sum())

    # delivre: la somme des produits qui ont delivre=1
    total_delivre = float(filtered_df['delivre'].sum())

    # stockDisponible: instock + delivre
    stock_disponible = float(total_instock + total_delivre)

    # Commande en cours: les produits qui en encours=1
    commande_en_cours = float(filtered_df['enCours'].sum())

    # vente: les produits ou vente=1
    total_vente = float(filtered_df['vente'].sum())

    # total_days = (pd.to_datetime(df['date']).max() - pd.to_datetime(df['date']).min()).days + 1

    # rythme de vente: le rythme de vente de tous les produits (vente/le nombre de jours total)
    rythme_de_vente = round(float(total_vente) / weekdays_count, 1)

    # remplacement: le nombre de produits où la colonne new-Rework=rework et vente=1
    remplacement = float(filtered_df[(df['new-Rework'] == 'rework') & (df['vente'] == 1)].shape[0])

    # rythme de remplacement: remplacement/nbr jours hors dimanche
    rythme_de_remplacement = round(float(remplacement) / weekdays_count, 1)

    destockage = float(total_vente + remplacement)

    rythme_de_destockage = round(float(destockage) / weekdays_count, 1)

    couverture = round(float(stock_disponible) / rythme_de_destockage, 1)

    return {
        "instock": total_instock,
        "delivre": total_delivre,
        "stockDisponible": stock_disponible,
        "Commande en cours": commande_en_cours,
        "vente": total_vente,
        "rythme de vente": rythme_de_vente,
        "remplacement": remplacement,
        "rythme de remplacement": rythme_de_remplacement,
        "destockage": destockage,
        "rythme de destockage": rythme_de_destockage,
        "couverture": couverture,
        "weekdays_without_sundays": weekdays_count
    }


def calculate_store_metrics(csv_file_path, date_range_str=""):
    start_date, end_date = parse_date_range(date_range_str)
    df = pd.read_csv(csv_file_path)

    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Skip filtering if start_date and end_date are None
    if start_date is None and end_date is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    store_metrics = {}
    # Calculate the number of non-Sunday days within the specified date range
    weekdays_count = count_non_sunday_days(date_range_str)

    for store in filtered_df['store'].unique():
        store_df = filtered_df[filtered_df['store'] == store]

        total_instock = float(store_df['instock'].sum())
        total_delivre = float(store_df['delivre'].sum())
        stock_disponible = float(total_instock + total_delivre)
        commande_en_cours = float(store_df['enCours'].sum())
        total_vente = float(store_df['vente'].sum())

        total_days = (pd.to_datetime(store_df['date']).max() - pd.to_datetime(store_df['date']).min()).days + 1
        rythme_de_vente = round(float(total_vente) / weekdays_count, 1)

        remplacement = float(store_df[(store_df['new-Rework'] == 'rework') & (store_df['vente'] == 1)].shape[0])
        rythme_de_remplacement = round(float(remplacement) / weekdays_count, 1)

        # destockage: toujours égal à idk
        destockage = float(total_vente + remplacement)

        # rythme de destockage: tjrs = idk
        rythme_de_destockage = round(float(destockage) / weekdays_count, 1)

        if rythme_de_destockage == 0:
            couverture = 0
        else:
            couverture = round(float(stock_disponible) / rythme_de_destockage, 1)

        store_metrics[store] = {
            "instock": total_instock,
            "delivre": total_delivre,
            "stockDisponible": stock_disponible,
            "Commande en cours": commande_en_cours,
            "vente": total_vente,
            "rythme de vente": rythme_de_vente,
            "remplacement": remplacement,
            "rythme de remplacement": rythme_de_remplacement,
            "destockage": destockage,
            "rythme de destockage": rythme_de_destockage,
            "couverture": couverture
        }

    return store_metrics


'''
def selected_canal_table(store_name: str, desired_stock_coverage: float, date_range_str="") -> dict:
    """
    Calculate the required metrics for a specific store based on the desired stock coverage.

    Parameters:
    - store_name: The name of the store for which the metrics should be calculated.
    - desired_stock_coverage: The desired stock coverage value.

    Returns:
    A dictionary containing the store name and the calculated metrics.
    """

    start_date, end_date = parse_date_range(date_range_str)
    # Assuming calculate_store_metrics returns a dictionary with store names as keys
    store_metrics = calculate_store_metrics(csv_file_path, date_range_str)

    # Check if the store exists in the metrics
    if store_name not in store_metrics:
        raise ValueError(f"Store '{store_name}' not found in the dataset.")

    # Retrieve the metrics for the specific store
    store_metric = store_metrics[store_name]

    # Calculate the required metrics
    vente_sur_la_periode_souhaite = store_metric["rythme de vente"] * desired_stock_coverage
    remplacement_sur_la_periode_souhaite = store_metric["rythme de remplacement"] * desired_stock_coverage
    besoin_en_stock_new = vente_sur_la_periode_souhaite - store_metric["instock"]
    besoin_en_stock_rework = remplacement_sur_la_periode_souhaite - store_metric["remplacement"]

    # Return the store name and the calculated metrics as a dictionary
    return {
        "store_name": store_name,
        "VentePS": vente_sur_la_periode_souhaite,
        "RemplacementPS": remplacement_sur_la_periode_souhaite,
        "BesoinNew": besoin_en_stock_new,
        "BesoinRework": besoin_en_stock_rework,
    }
'''


def selected_canal_table_multiple_stores(store_names: List[str], desired_stock_coverage: float, date_range_str="",
                                         canal=None, store=None, categorie=None, sousCat=None,
                                         nomArticle=None, newRework=None) -> \
        List[dict]:
    """
    Calculate the required metrics for multiple stores based on the desired stock coverage.

    Parameters:
    - store_names: A list of store names for which the metrics should be calculated.
    - desired_stock_coverage: The desired stock coverage value.
    - date_range_str: Optional parameter for specifying the date range. Default is an empty string.

    Returns:
    A list of dictionaries, each containing the store name and the calculated metrics.
    """

    start_date, end_date = parse_date_range(date_range_str)
    # Assuming calculate_store_metrics returns a dictionary with store names as keys
    store_metrics = calculate_store_metrics2(csv_file_path, date_range_str, canal=None, store=None, categorie=None,
                                             sousCat=None,
                                             nomArticle=None, newRework=None)

    results = []

    for store_name in store_names:
        # Check if the store exists in the metrics
        if store_name not in store_metrics:
            raise ValueError(f"Store '{store_name}' not found in the dataset.")

        # Retrieve the metrics for the specific store
        store_metric = store_metrics[store_name]

        # Calculate the required metrics
        vente_sur_la_periode_souhaite = store_metric["rythme de vente"] * desired_stock_coverage
        remplacement_sur_la_periode_souhaite = store_metric["rythme de remplacement"] * desired_stock_coverage
        besoin_en_stock_new = math.ceil(vente_sur_la_periode_souhaite - store_metric["instock"])
        besoin_en_stock_rework = math.ceil(remplacement_sur_la_periode_souhaite - store_metric["remplacement"])

        # Append the store name and the calculated metrics as a dictionary to the results list
        results.append({
            "store_name": store_name,
            "VentePS": vente_sur_la_periode_souhaite,
            "RemplacementPS": remplacement_sur_la_periode_souhaite,
            "BesoinNew": besoin_en_stock_new,
            "BesoinNewSouhaite": besoin_en_stock_new,
            "BesoinRework": besoin_en_stock_rework,
            "BesoinReworkSouhaite": besoin_en_stock_rework
        })

    return results


# -----------------------NEW----------------------

def apply_filters(df, canal=None, store=None, categorie=None, sousCat=None, nomArticle=None, newRework=None):
    if canal:
        channels = canal.split(', ')
        df = df[df['canal'].isin(channels)]
    if store:
        stores = store.split(', ')
        df = df[df['store'].isin(stores)]
    if categorie:
        categories = categorie.split(', ')
        df = df[df['categorie'].isin(categories)]
    if sousCat:
        sousCats = sousCat.split(', ')
        df = df[df['sousCat'].isin(sousCats)]
    if nomArticle:
        nomArticles = nomArticle.split(', ')
        df = df[df['nomArticle'].isin(nomArticles)]
    if newRework:
        newReworks = newRework.split(', ')
        df = df[df['new-Rework'].isin(newReworks)]
    return df


def calculate_metrics2(csv_file_path, date_range_str="", canal=None, store=None, categorie=None, sousCat=None,
                       nomArticle=None, newRework=None):
    start_date, end_date = parse_date_range(date_range_str)
    df = pd.read_csv(csv_file_path)

    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Skip filtering if start_date and end_date are None
    if start_date is None and end_date is None:
        filtered_df = df.copy()
        # Use the full date range of the data for counting weekdays
        start_date = df['date'].min()
        end_date = df['date'].max()
    else:
        # Now perform the filtering
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Apply filters based on the provided parameters
    filtered_df = apply_filters(filtered_df, canal=canal, store=store, categorie=categorie, sousCat=sousCat,
                                nomArticle=nomArticle, newRework=newRework)

    # Calculate the number of non-Sunday days within the specified date range
    weekdays_count = count_non_sunday_days(date_range_str)

    # instock: la somme des produits qui sont instock
    total_instock = float(filtered_df['instock'].sum())

    # delivre: la somme des produits qui ont delivre=1
    total_delivre = float(filtered_df['delivre'].sum())

    # stockDisponible: instock + delivre
    stock_disponible = float(total_instock + total_delivre)

    # Commande en cours: les produits qui en encours=1
    commande_en_cours = float(filtered_df['enCours'].sum())

    # vente: les produits ou vente=1
    total_vente = float(filtered_df['vente'].sum())

    # total_days = (pd.to_datetime(df['date']).max() - pd.to_datetime(df['date']).min()).days + 1

    # rythme de vente: le rythme de vente de tous les produits (vente/le nombre de jours total)
    rythme_de_vente = round(float(total_vente) / weekdays_count, 1)

    # remplacement: le nombre de produits où la colonne new-Rework=rework et vente=1
    remplacement = float(filtered_df[(df['new-Rework'] == 'rework') & (df['vente'] == 1)].shape[0])

    # rythme de remplacement: remplacement/nbr jours hors dimanche
    rythme_de_remplacement = round(float(remplacement) / weekdays_count, 1)

    destockage = float(total_vente + remplacement)

    rythme_de_destockage = round(float(destockage) / weekdays_count, 1)

    if rythme_de_destockage == 0:
        couverture = 0
    else:
        couverture = round(float(stock_disponible) / rythme_de_destockage, 1)

    return {
        "instock": total_instock,
        "delivre": total_delivre,
        "stockDisponible": stock_disponible,
        "Commande en cours": commande_en_cours,
        "vente": total_vente,
        "rythme de vente": rythme_de_vente,
        "remplacement": remplacement,
        "rythme de remplacement": rythme_de_remplacement,
        "destockage": destockage,
        "rythme de destockage": rythme_de_destockage,
        "couverture": couverture,
        "weekdays_without_sundays": weekdays_count
    }


def calculate_store_metrics2(csv_file_path, date_range_str="", canal=None, store=None, categorie=None, sousCat=None,
                             nomArticle=None, newRework=None):
    start_date, end_date = parse_date_range(date_range_str)
    df = pd.read_csv(csv_file_path)

    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Skip filtering if start_date and end_date are None
    if start_date is None and end_date is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Apply filters based on the provided parameters
    filtered_df = apply_filters(filtered_df, canal=canal, store=store, categorie=categorie, sousCat=sousCat,
                                nomArticle=nomArticle, newRework=newRework)

    store_metrics: Dict[str, dict] = {}
    # Calculate the number of non-Sunday days within the specified date range
    weekdays_count = count_non_sunday_days(date_range_str)

    for store in filtered_df['store'].unique():
        store_df = filtered_df[filtered_df['store'] == store]

        total_instock = float(store_df['instock'].sum())
        total_delivre = float(store_df['delivre'].sum())
        stock_disponible = float(total_instock + total_delivre)
        commande_en_cours = float(store_df['enCours'].sum())
        total_vente = float(store_df['vente'].sum())

        total_days = (pd.to_datetime(store_df['date']).max() - pd.to_datetime(store_df['date']).min()).days + 1
        rythme_de_vente = round(float(total_vente) / weekdays_count, 1)

        remplacement = float(store_df[(store_df['new-Rework'] == 'rework') & (store_df['vente'] == 1)].shape[0])
        rythme_de_remplacement = round(float(remplacement) / weekdays_count, 1)

        # destockage: toujours égal à idk
        destockage = float(total_vente + remplacement)

        # rythme de destockage: tjrs = idk
        rythme_de_destockage = round(float(destockage) / weekdays_count, 1)

        if rythme_de_destockage == 0:
            couverture = 0
        else:
            couverture = round(float(stock_disponible) / rythme_de_destockage, 1)

        store_metrics[store] = {
            "instock": total_instock,
            "delivre": total_delivre,
            "stockDisponible": stock_disponible,
            "Commande en cours": commande_en_cours,
            "vente": total_vente,
            "rythme de vente": rythme_de_vente,
            "remplacement": remplacement,
            "rythme de remplacement": rythme_de_remplacement,
            "destockage": destockage,
            "rythme de destockage": rythme_de_destockage,
            "couverture": couverture
        }

    return store_metrics

# -------------------- Dispatching----------------------------------


def return_received_data(received_data: List[Dict]) -> List[Dict]:
    """
    Returns the received data unchanged.

    Args:
    - received_data (List[Dict]): A list of dictionaries representing the data received from the Angular server.

    Returns:
    - List[Dict]: The original received data.
    """
    return received_data