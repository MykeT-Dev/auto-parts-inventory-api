# Auto Parts Inventory API

A REST API for managing an auto parts inventory system, including parts listings, categories, sellers, and vehicle compatibility.

This project focuses on backend system design, relational database modeling, and building a clean, maintainable API layer that reflects real-world use cases.

---

## Project Overview

This project simulates a real-world inventory and parts lookup system used in service and parts departments.

The system is designed to handle structured data relationships between parts, vehicles, and categories, allowing users to query compatible parts based on vehicle attributes such as make, model, and year.

---

## Key Features

- Retrieve parts listings (applications)
- Query individual records by ID
- Vehicle-based part lookup using make, model, and year
- Optional filtering by category and price range
- Pagination support for large datasets
- Normalized relational database design
- Clean API layer using FastAPI
- SQLite-backed persistence

---

## Tech Stack

- Python 3
- FastAPI
- SQLite
- SQL

---

## Project Structure

data_raw/        # Source dataset (CSV files)  
docs/            # Documentation (ERD, project requirements)  
fetch_data.py    # Data ingestion script  
audit_data.py    # Data validation script  
load_data.py     # Loads data into database  
main.py          # FastAPI application  
schema.sql       # Database schema  
queries.sql      # SQL queries  
requirements.txt # Project dependencies  

---

## Database Design

The system is built using a normalized relational schema to model:

- Applications (parts listings)
- Product categories
- Sellers
- Vehicles
- Compatibility relationships between parts and vehicles

See `docs/erd.md` for the full entity relationship diagram.

---

## How to Run This Project

**1. Clone the repository**

    git clone https://github.com/MykeT-Dev/auto-parts-inventory-api.git  
    cd auto-parts-inventory-api  

**2. Create a virtual environment**

    python -m venv venv  
    venv\Scripts\activate  

**3. Install dependencies**

    pip install -r requirements.txt  

**4. Run the API**

    python -m uvicorn main:app --reload  

**5. Open in browser**

    http://127.0.0.1:8000/docs  

---

## API Usage Examples

Once the server is running, the API can be explored using the built-in Swagger UI.

![Swagger UI Overview](assets/swagger-overview.png)

### Get all applications

GET /applications?limit=10

### Get a single application

GET /applications/{app_id}

Example:

GET /applications/10074150

### Lookup parts by vehicle

This endpoint reflects a real-world workflow where parts are searched based on vehicle compatibility rather than part number.

![Parts Endpoint Query](assets/swagger-parts-query.png)

GET /parts?make=ford&model=mustang&year=2000

### With filters and pagination

GET /parts?make=ford&model=mustang&year=2000&page=1&page_size=20

#### Example Response

[
  {
    "app_id": 11122296,
    "headline": "FORD Mustang 1999-2003",
    "price_usd": 83,
    "vehicle_model": "Mustang",
    "vehicle_id": 517,
    "category": "Headlight"
  }
]
---

## Current Status

The core API and database pipeline are fully functional and stable.

Current focus:
- Presenting the API for portfolio demonstration
- Code cleanup and documentation

---

## Next Steps

- Introduce a frontend UI for interacting with the API
- Enhance filtering capabilities (e.g., partial text search)
- Deploy the API for public access

---

## Author

Myke Turza