from fastapi import FastAPI, HTTPException
import sqlite3
import os

app = FastAPI(
    title="Live Crypto Market Data API",
    description="A production-ready REST API that serves structural data from our automated pipeline.",
    version="1.0.0"
)

DB_NAME = os.getenv("DB_NAME", "market_data.db")

def get_db_connection():
    """Establishes a connection to the SQLite database with row factory mapping."""
    try:
        conn = sqlite3.connect(DB_NAME)
        # This converts database tuples into accessible Python dictionaries
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

@app.get("/")
def read_root():
    """Root endpoint verifying API health status."""
    return {
        "status": "online",
        "message": "Welcome to the Crypto Data Pipeline API. Access /prices to fetch records or /docs for interactive documentation."
    }

@app.get("/prices")
def get_all_prices():
    """Fetches and returns all ingested crypto data records from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, current_price, market_cap, last_updated, ingested_at FROM crypto_prices")
        rows = cursor.fetchall()
        
        # Convert rows into a clean, serializable list of dictionaries
        data = [dict(row) for row in rows]
        return {"count": len(data), "data": data}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")
    finally:
        conn.close()

@app.get("/prices/{crypto_id}")
def get_price_by_id(crypto_id: str):
    """Fetches a specific cryptocurrency record using its unique string ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, name, current_price, market_cap, last_updated, ingested_at FROM crypto_prices WHERE id = ?", 
            (crypto_id.lower(),)
        )
        row = cursor.fetchone()
        
        if row is None:
            raise HTTPException(status_code=404, detail=f"Cryptocurrency with ID '{crypto_id}' not found in database.")
            
        return dict(row)
    finally:
        conn.close()