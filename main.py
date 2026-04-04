from fastapi import FastAPI, Query, HTTPException, params
from typing import Optional, List
import sqlite3

# Initialize FastAPI application
app = FastAPI()

# Path to SQLite database
DB_PATH = "database.db"

# Helper function to create a database connection
def get_connection():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    # Return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row 
    return conn

# Root endpoint for testing
@app.get("/")
def root():
    return {"message": "Welcome to the Parts Master API!"}

# Endpoint to get a list of applications with optional limit
@app.get("/applications")
def get_applications(limit: int = Query(10, ge=1, le=100)):
    # Connect to database
    conn = get_connection()
    cursor = conn.cursor()

    # Query the applications table, limit results by `limit` parameter
    rows = cursor.execute("""
        SELECT app_id, headline, price_usd
        FROM applications
        LIMIT ?
    """, (limit,)).fetchall()

    # Close the database connection
    conn.close()

    # Convert each row to a dictionary and return as JSON
    return [dict(row) for row in rows] 

# Endpoint to get details of a single application by ID
@app.get("/applications/{app_id}")
def get_application(app_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Query for a single application by its ID
    row = cursor.execute("""
        SELECT app_id, headline, price_usd
        FROM applications
        WHERE app_id = ?
    """, (app_id,)).fetchone()

    conn.close()

    # Return error if no application found
    if row is None:
        return {"error": "Application not found"}

    # Return application data as JSON
    return {
        "app_id": row[0],
        "headline": row[1],
        "price_usd": row[2]
    }

# Endpoint to lookup parts compatible with a vehicle
@app.get("/parts")
def get_parts(
    make: Optional[str] = None,
    model: Optional[str] = None,
    year: Optional[int] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Lookup parts compatible with a vehicle (make, model, year)
    Optional filters: category, min_price, max_price
    Supports pagination
    """
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    conn = get_connection()
    cursor = conn.cursor()

    # Base query: join applications, compatibility, vehicles, and product_category
    query = """
    SELECT a.app_id, a.headline, a.price_usd, v.model_name, v.id as vehicle_id, pc.category_name
    FROM applications a
    JOIN compatibility c ON a.app_id = c.app_id
    JOIN vehicles v ON c.vehicles_id = v.id
    JOIN product_category pc ON a.category_id = pc.id
    WHERE 1=1
    """

    # Parameters for SQL query
    params: List = []

    # Add optional filters if provided

    if make:
        query += " AND LOWER(v.manufacturer_name) LIKE LOWER(?)"
        params.append(F"%{make}%")

    if model:
        query += " AND LOWER(v.model_name) LIKE LOWER(?)"
        params.append(F"%{model}%")

    if year is not None:
        query += " AND ? BETWEEN c.bottom_year AND c.top_year"
        params.append(year)

    if category:
        query += " AND pc.category_name = ?"
        params.append(category)
    if min_price is not None:
        query += " AND a.price_usd >= ?"
        params.append(min_price)
    if max_price is not None:
        query += " AND a.price_usd <= ?"
        params.append(max_price)

    # Add pagination limits
    query += " LIMIT ? OFFSET ?"
    params.extend([page_size, offset])

    # Execute query and fetch results
    rows = cursor.execute(query, params).fetchall()
    conn.close()

    # Raise error if no parts found
    if not rows:
        raise HTTPException(status_code=404, detail="No compatible parts found")

    # Return results as JSON list
    return [
        {
            "app_id": row["app_id"],
            "headline": row["headline"],
            "price_usd": row["price_usd"],
            "vehicle_model": row["model_name"],
            "vehicle_id": row["vehicle_id"],
            "category": row["category_name"]
        }
        for row in rows
    ]

@app.get("/debug/counts")
def debug_counts():
    conn = get_connection()
    cursor = conn.cursor()

    apps = cursor.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    compat = cursor.execute("SELECT COUNT(*) FROM compatibility").fetchone()[0]
    vehicles = cursor.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]

    conn.close()

    return {
        "applications": apps,
        "compatibility": compat,
        "vehicles": vehicles
    }