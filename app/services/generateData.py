import pandas as pd
import numpy as np
from datetime import datetime

# Create an empty list to store the data
data = []

# Lists of boutiques and stores for franchises
boutiques = ["boutique Tunis", "boutique Bizerte", "boutique Sousse", "boutique Hammamet",
             "boutique Kasserine", "boutique Djerba", "boutique Kairouan", "boutique Jendouba"]
stores = ["store A", "store B", "store C", "store D", "store E", "store F", "store G", "store H"]

# Categories
categories = ["smartphone", "mbb"]

# Sub-categories and product names
sub_categories = {
    "smartphone": {
        "samsung": ["SAMSUNG GALAXY A55", "SAMSUNG GALAXY A35", "SAMSUNG GALAXY S24"],
        "xiaomi": ["XIAOMI REDMI A3", "XIAOMI REDMI NOTE 13", "XIAOMI REDMI 13C"],
        "oppo": ["OPPO A38", "OPPO RENO 11F", "OPPO A18"],
        "infinix": ["INFINIX HOT 40", "INFINIX SMART 7"]
    },
    "mbb": {
        "flybox": ["Flybox 42 Go", "Flybox 55 Go", "Flybox 75 Go"],
        "fixbox": ["Fixbox Premium"],
        "airbox": ["Airbox 55 Go", "Airbox 100 Go", "Airbox 150 Go"]
    }
}

today = datetime.now().date()
# Start and end dates
start_date = pd.to_datetime("2022-08-01")
end_date = pd.to_datetime(today)

# Generate all dates between start and end
dates = pd.date_range(start_date, end_date, freq='MS')

# Loop to generate data for each boutique/store, month, and category/sub-category/product
for boutique in boutiques:
    for date in dates:
        for category in categories:
            for sub_category, items in sub_categories[category].items():
                for item in items:
                    # Randomly choose between boutique and franchise
                    canal = np.random.choice(['Boutique', 'Franchise'], p=[0.8, 0.2])  # Adjusting probabilities as needed

                    if category == "smartphone":
                        new_rework = "new"
                        quantity = np.random.randint(3, 13)
                    else:  # category == "mbb"
                        new_rework = np.random.choice(["new", "rework"])
                        quantity = np.random.randint(10, 21)
                    instock = np.random.randint(0, 2)
                    delivre = np.random.randint(0, 2)
                    enCours = np.random.randint(0, 2)
                    vente = 0 if instock == 1 else (np.random.randint(0, 2) if delivre == 1 else 0)

                    # Assign boutique or store based on canal
                    if canal == 'Boutique':
                        store = boutique
                    else:  # canal == 'Franchise'
                        store = np.random.choice(stores)

                    # Append data in the correct order
                    data.append([canal, store, date.strftime("%Y-%m-%d"), category, sub_category, item, new_rework, quantity, instock, delivre, enCours, vente])

# Convert the data to DataFrame
df = pd.DataFrame(data, columns=["Canal", "Store", "Date", "Categorie", "SousCat", "NomArticle", "new-Rework", "Quantite", "Instock", "Delivre", "EnCours", "Vente"])

# Function to determine the replacement value
def determine_replacement(row):
    if row['Categorie'] == 'smartphone':
        return 0
    elif row['Categorie'] == 'mbb':
        if row['Vente'] == 1:
            return 0
        else:
            return np.random.randint(0, 2)

# Apply the function to each row of the DataFrame
df['remplacement'] = df.apply(determine_replacement, axis=1)

# Display the DataFrame
print(df)

# Export the DataFrame to a CSV file
df.to_csv('dataFinale.csv', index=False)
