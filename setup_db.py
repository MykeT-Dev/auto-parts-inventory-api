import sqlite3
from load_data import main as load_data_main

DB_PATH = "database.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    print("Database tables created successfully.")

def main():
    print("Setting up the database...")

    create_tables()
    load_data_main()

    print("Database setup complete.")

if __name__ == "__main__":
    main()

