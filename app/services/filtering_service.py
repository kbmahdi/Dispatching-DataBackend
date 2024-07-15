import pandas as pd
import numpy as np

# Assuming csv_file_path is defined globally as shown in your csv_service.py
csv_file_path = 'app/data/test.csv'


def get_filtered_data(date_filter=None, store_nbr_filter=None, family_filter=None, onpromotion_filter=None):
    # Read the CSV file using the global csv_file_path
    df = pd.read_csv(csv_file_path)

    # Convert 'onpromotion' to integer for proper comparison
    df['onpromotion'] = df['onpromotion'].astype(int)

    # Apply filters
    if date_filter is not None:
        df = df[df['date'] == date_filter]
    if store_nbr_filter is not None:
        df = df[df['store_nbr'] == store_nbr_filter]
    if family_filter is not None:
        df = df[df['family'] == family_filter]
    if onpromotion_filter is not None:
        df = df[df['onpromotion'] == onpromotion_filter]

    # Convert filtered DataFrame to dictionary
    filtered_data = df.to_dict('records')

    return filtered_data
