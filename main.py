from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_PATH = "database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 🔥 important
    return conn

@app.get("/")
def root():
    return {"message": "Welcome to the Parts Master API!"}

@app.get("/applications")
def get_applications(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT app_id, headline, price_usd
        FROM applications
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return [dict(row) for row in rows] 

@app.get("/applications/{app_id}")
def get_application(app_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    row = cursor.execute("""
        SELECT app_id, headline, price_usd
        FROM applications
        WHERE app_id = ?
    """, (app_id,)).fetchone()

    conn.close()

    if row is None:
        return {"error": "Application not found"}

    return {
        "app_id": row[0],
        "headline": row[1],
        "price_usd": row[2]
    }