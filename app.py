import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Crypto Data Pipeline REST API")
DB_NAME = "market_data.db"

def get_db_connection():
    """Establishes a connection to the database with a row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables fetching rows as dictionaries
    return conn

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crypto Data API. Go to /prices or /docs to view data."}

@app.get("/prices")
def get_prices():
    """Retrieves all ingested cryptocurrency price metrics from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query matching our updated database column schema
        cursor.execute("""
            SELECT id, coin_id, price_usd, change_24h, ingested_at 
            FROM crypto_prices 
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows into a clean, serialized JSON array
        data_list = [dict(row) for row in rows]
        
        return {
            "count": len(data_list),
            "data": data_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")