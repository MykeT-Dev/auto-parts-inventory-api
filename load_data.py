import sqlite3
import csv
from pathlib import Path

DB_PATH = "database.db"
DATA_DIR = Path("data_raw")

def get_connection():
    return sqlite3.connect(DB_PATH)


def load_csv(cursor, table_name, file_path, columns):
    with open(file_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        rows = []

        for row in reader:
            new_row = []

            for col in columns:
                if col == "in_stock":
                    new_row.append(1)

                elif table_name == "vehicle_type" and col == "vehicle_type_name":
                    new_row.append(row["type_name"])


                elif table_name == "compatibility" and col == "vehicle_id":
                    new_row.append(row["vehicles_id"])

                else:
                    new_row.append(row[col])

            rows.append(tuple(new_row))                

    placeholders = ",".join(["?"] * len(columns))
    query = f"INSERT OR IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    cursor.executemany(query, rows)

def main():
    conn = get_connection()
    cursor = conn.cursor()

    # Load lookup tables first
    load_csv(
        cursor,
        "product_category",
        DATA_DIR / "product_category.csv",
        ["id", "category_name"]
    )

    load_csv(
        cursor,
        "seller",
        DATA_DIR / "seller.csv",
        ["id", "seller_name"]
    )

    load_csv(
        cursor,
        "application_status",
        DATA_DIR / "application_status.csv",
        ["id", "status_name"]
    )

    load_csv(
        cursor,
        "vehicle_type",
        DATA_DIR / "vehicle_type.csv",
        ["id", "vehicle_type_name"]  # ✅ FIXED
    )

    # Dependent tables
    load_csv(
        cursor,
        "vehicles",
        DATA_DIR / "vehicles.csv",
        ["id", "model_name", "manufacturer_name", "vehicle_type_id"]  # ✅ REMOVED year
    )

    load_csv(
        cursor,
        "applications",
        DATA_DIR / "applications.csv",
        [
            "app_id",
            "headline",
            "price_usd",
            "category_id",
            "seller_id",
            "status_id",
            "vehicle_type_id",
            "in_stock"
        ]
    )

    # Bridge table last
    load_csv(
        cursor,
        "compatibility",
        DATA_DIR / "compatibility.csv",
        ["app_id", "vehicle_id"]
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()