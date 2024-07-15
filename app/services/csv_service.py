import pandas as pd
import numpy as np

# Global variable for the CSV file path
csv_file_path = 'app/data/test.csv'  # Updated to match your project structure

# Function to prepare data for frontend
# Function to prepare data for frontend
def prepare_dropdown_data():
    # Read the CSV file using the global csv_file_path
    df = pd.read_csv(csv_file_path)

    # Convert 'onpromotion' to string
    df['onpromotion'] = df['onpromotion'].astype(str)

    # Extract unique values for each column
    unique_store_nbr = df['store_nbr'].unique().tolist()
    unique_families = df['family'].unique().tolist()
    unique_onpromotions = ['Yes', 'No']  # Assuming 'onpromotion' is binary

    # Combine all unique values into one list
    combined_unique_values = unique_store_nbr + unique_families + unique_onpromotions

    # Remove duplicates
    unique_combined_values = list(set(combined_unique_values))

    # Prepare data for frontend
    dropdown_data = {
        "store_nbr": [{"name": str(store_nbr)} for store_nbr in unique_store_nbr],
        "family": [{"name": family} for family in unique_families],
        "onpromotion": [{"name": promotion} for promotion in unique_onpromotions]
    }

    # Replace NaN values with None for JSON serialization
    for key in dropdown_data.keys():
        dropdown_data[key] = [{k: v if pd.notnull(v) else None for k, v in item.items()} for item in dropdown_data[key]]

    return dropdown_data