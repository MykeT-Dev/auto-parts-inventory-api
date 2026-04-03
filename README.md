# Auto Parts Inventory API

## Overview

This project is a REST API for managing an auto parts inventory system. It is built around a normalized relational database schema that models relationships between parts, categories, sellers, and vehicle compatibility.

The project uses a real-world dataset and focuses on backend design, data modeling, and building a clean, maintainable system.

---

## Features

* Manage parts listings (applications)
* Organize parts by category
* Track sellers and listing status
* Model compatibility between parts and vehicles
* Maintain inventory availability

---

## Database Design

The database schema is normalized and designed to reflect real-world relationships.

Core entities include:

* Applications (parts listings)
* Product categories
* Sellers
* Application status
* Vehicle types and vehicles
* Compatibility (many-to-many relationship between parts and vehicles)

See `docs/erd.md` for the full entity relationship diagram.

---

## Tech Stack

* Python
* SQL
* Git

---

## Project Structure

```
data_raw/           # Source dataset (CSV files)
docs/               # Documentation (ERD, requirements)
fetch_data.py       # Data ingestion script
audit_data.py       # Data validation script
schema.sql          # Database schema (in progress)
```

---

## Status

In progress. Current focus is on implementing the database schema and core API functionality.

---

## Author

Myke Turza
