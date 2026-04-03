# Auto Parts Inventory API

A REST API for managing an auto parts inventory system, including parts listings, categories, sellers, and vehicle compatibility.

This project focuses on backend system design, database modeling, and building a clean, maintainable API layer.

---

## Overview

This project simulates a real-world inventory management system.

The API is built on top of a normalized relational database and exposes endpoints for querying parts data and relationships between entities.

---

## Features

- Retrieve parts listings (applications)
- Query individual records by ID
- Structured relational database design
- Clean API layer using FastAPI
- SQLite-backed persistence

---

## API Usage

Once the server is running, access the interactive documentation:

http://127.0.0.1:8000/docs

### Example Endpoints

Get all applications:  
GET /applications?limit=10

Get a single application:  
GET /applications/{app_id}

Example:  
GET /applications/10074150

---

## Tech Stack

- Python
- FastAPI
- SQLite
- SQL

---

## Project Structure

data_raw/        # Source dataset (CSV files)  
docs/            # Documentation (ERD, requirements)  
fetch_data.py    # Data ingestion script  
audit_data.py    # Data validation script  
load_data.py     # Loads data into database  
main.py          # FastAPI application  
schema.sql       # Database schema  
queries.sql      # SQL queries  

---

## Database Design

The system is built using a normalized relational schema to model:

- Applications (parts listings)
- Categories
- Sellers
- Vehicles
- Compatibility relationships

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

pip install fastapi uvicorn  

**4. Run the API**

python -m uvicorn main:app --reload  

**5. Open in browser**

http://127.0.0.1:8000/docs  

---

## Current Status

In progress. Current focus:

- Expanding API endpoints
- Improving query performance
- Preparing for frontend integration

---

## Next Steps

- Add filtering (by category, price range, vehicle)
- Add pagination
- Introduce a frontend UI
- Deploy API

---

## Author

Myke Turza