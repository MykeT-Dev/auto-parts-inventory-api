from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
import sqlite3
import os
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from setup_db import setup_database


# Initialize FastAPI application
app = FastAPI()


# Path to SQLite database
DB_PATH = "database.db"

def initialize_database():
    """
    Check if the database file exists. If not, create it and set up tables.
    This ensures the database is ready when the app starts.
    """
    if not os.path.exists(DB_PATH):
        print("Database file not found. Initializing database...")
        setup_database()
    else:
        print("Database file found. Skipping initialization.")

# AUTH Configuration

# Secret key for JWT encoding/decoding
# For local deployment, it falls back to "dev-secret-key"
# For deployment, set SECRET_KEY as an environment variable
SECRET_KEY = os.getenv("SECRET_KEY","dev-secret-key")

# Algorithm used for JWT
ALGORITHM = "HS256"

# Token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Fake user database for demonstration purposes
fake_users_db = {
    "admin": {
        "username": "admin",

        # Hash the password using bcrypt
        # Note: This will generate a different hash each time the app runs
        "hashed_password": pwd_context.hash("admin123"),

        # Role is used for access control (e.g., admin vs regular user)
        "role": "admin"
    },
    "user": {
        "username": "user",
        "hashed_password": pwd_context.hash("user123"),
        "role": "user"
    }
}    

# Authentication functions

# Verify a plain password against a hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user by username and password
def authenticate_user(username: str, password: str):
    # Look up user in fake database
    user = fake_users_db.get(username)
    # If user not found or password doesn't match, return None
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    # Return user dict if authentication successful
    return user

# Create a JWT access token for a user
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Copy the data
    to_encode = data.copy()

    # Set expiration time for the token
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Login Endpoint

# endpoint handles user login and returns a JWT token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible login endpoint.
    
    Expects:
    - username
    - password
    
    Returns:
    -JWT access token if credentials are valid
    """

    # Authenticate the user using the helper function
    user = authenticate_user(form_data.username, form_data.password)

    # If authentication fails, raise an HTTP 401 Unauthorized
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    # Create a JWT token with user data
    access_token = create_access_token(
        data={
            "sub": user["username"],
            "role": user["role"]
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Return the tokem in standard OAuth2 format
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extract and validate the user from the JWT token
    """

    # Default exception if token is invalid
    credentials_exceptiion = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user info
        username = payload.get("sub")
        role = payload.get("role")

        # If no username, token is invalid
        if username is None:
            raise credentials_exceptiion
        
    except JWTError:
        # Token is invalid or expired
        raise credentials_exceptiion

    # return user data
    return {
        "username": username,
        "role": role
    }

# Require admin role for certain endpoints
def require_admin(current_user: dict = Depends(get_current_user)):
    """
    Ensures the user has admin privileges
    """

    # Check if the user's role is NOT admin
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    # If user is admin, allow access
    return current_user

# Request model for adding a new part
# Tells FASTAPI what fields are required when sending a POST request
class PartCreate(BaseModel):
    headline: str
    price_usd: float
    category_id: int
    seller_id: int
    status_id: int
    vehicle_type_id: int
    in_stock: int
    vehicles_id: int
    bottom_year: Optional[int] = None
    top_year: Optional[int] = None

# Helper function to create a database connection
def get_connection():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    # Return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row 
    return conn

@app.on_event("startup")
def startup_event():
    """
    FastAPI startup event handler.
    This runs when the application starts and ensures the database is initialized.
    """
    initialize_database()

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
    part_name: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),

    # Requires authentication for this enpoint
    current_user: dict = Depends(get_current_user)
):
    """
    Lookup parts compatible with a vehicle (make, model, year)

    Optional filters: 
    - category 
    - min_price
    - max_price
    - part_name

    Supports pagination
    """

    # Calculate offset for pagination
    offset = (page - 1) * page_size

    # Connect to database
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

    # Filter by vehicle make (manufacturer_name)
    if make:
        query += " AND LOWER(v.manufacturer_name) LIKE LOWER(?)"
        params.append(F"%{make}%")

    # Filter by vehicle model
    if model:
        query += " AND LOWER(v.model_name) LIKE LOWER(?)"
        params.append(F"%{model}%")

    # Filter by model year fitting range
    if year is not None:
        query += " AND ? BETWEEN c.bottom_year AND c.top_year"
        params.append(year)

    # Filter by category name
    if category:
        query += " AND pc.category_name = ?"
        params.append(category)

    # Filter by minimum price
    if min_price is not None:
        query += " AND a.price_usd >= ?"
        params.append(min_price)

    # Filter by maximum price
    if max_price is not None:
        query += " AND a.price_usd <= ?"
        params.append(max_price)

    # Filter by part name in headline
    if part_name:
        query += """
        AND (
            LOWER(a.headline) LIKE LOWER(?)
            OR LOWER(pc.category_name) LIKE LOWER(?)
        )
        """
        params.append(f"%{part_name}%")
        params.append(f"%{part_name}%")

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

# Add new part (Admin only)
@app.post("/parts")
def add_part(
    part: PartCreate,
    current_user: dict = Depends(require_admin)
):
    """
    Add a new part to the database (Admin only)

    This does two things:
    1. Inserts a new part into the applications table
    2. Link that part to a vehicle in the compatibility table
    """

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert into applications table
    cursor.execute("""
        INSERT INTO applications (
                   headline,
                   price_usd,
                   category_id,
                   seller_id,
                   status_id,
                   vehicle_type_id,
                   in_stock
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        part.headline,
        part.price_usd,
        part.category_id,
        part.seller_id,
        part.status_id,
        part.vehicle_type_id,
        part.in_stock
    ))

    # Get the new app_id
    # SQLite automatically generates this (AUTOINCREMENT)
    new_app_id = cursor.lastrowid

    # Insert into compatibility table to link part to vehicle
    cursor.execute("""
        INSERT INTO compatibility (
                   app_id,
                   vehicles_id,
                   bottom_year,
                   top_year
        ) VALUES (?, ?, ?, ?)
    """, (
        new_app_id,
        part.vehicles_id,
        part.bottom_year,
        part.top_year
    ))

    # Save changes
    conn.commit()

    # Close connection
    conn.close()

    return {
        "message": "Part added successfully",
        "app_id": new_app_id,
        "linked_vehicle": part.vehicles_id
    }
