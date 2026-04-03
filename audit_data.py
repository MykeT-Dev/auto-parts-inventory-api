import pandas as pd

def audit():
    # Load the main parts of the file
    apps = pd.read_csv('data_raw/applications.csv')
    # Load the categories file
    cats = pd.read_csv('data_raw/product_category.csv')

    print("--- APPLICATIONS (Main Inventory) ---")
    print(apps.head())
    print("\n--- CATEGORIES ---")
    print(cats.head())

if __name__ == "__main__":
    audit()    