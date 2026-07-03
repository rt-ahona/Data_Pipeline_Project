import requests
import sqlite3
import logging
import os
from datetime import datetime

# 1. Configure structured logging to track pipeline execution
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),  # Saves logs to a file for auditing
        logging.StreamHandler()              # Still prints to your Windsurf terminal
    ]
)

# 2. Externalize configurations (Standard practice for backend security)
DB_NAME = os.getenv("DB_NAME", "market_data.db")
API_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_crypto_data():
    """Fetches real-time market data with network exception handling."""
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 5,
        'page': 1
    }
    try:
        logging.info("Initiating API request to CoinGecko...")
        response = requests.get(API_URL, params=params, timeout=10) # Added timeout to prevent hanging
        response.raise_for_status()
        logging.info("Data successfully fetched from remote API.")
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("The request timed out. Check network latency.")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        logging.error(f"An unexpected network error occurred: {e}")
    return None

def setup_database():
    """Initializes the database using contextual connection management."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id TEXT PRIMARY KEY,
                name TEXT,
                current_price REAL,
                market_cap REAL,
                last_updated TEXT,
                ingested_at TEXT
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        logging.critical(f"Database initialization failed: {e}")
        raise

def save_to_database(conn, data):
    """Inserts processed data securely using parameterized queries to prevent SQL Injection."""
    if not data:
        logging.warning("No data provided to save.")
        return

    try:
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for item in data:
            cursor.execute('''
                INSERT OR REPLACE INTO crypto_prices (id, name, current_price, market_cap, last_updated, ingested_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (item['id'], item['name'], item['current_price'], item['market_cap'], item['last_updated'], current_time))
        
        conn.commit()
        logging.info(f"Successfully ingested {len(data)} records into the database.")
    except sqlite3.Error as e:
        logging.error(f"Failed to insert data into database: {e}")
        conn.rollback() # Rolls back changes if an error happens to protect data integrity

if __name__ == "__main__":
    logging.info("=== Data Pipeline Process Started ===")
    raw_data = fetch_crypto_data()
    
    if raw_data:
        try:
            db_connection = setup_database()
            save_to_database(db_connection, raw_data)
        finally:
            if 'db_connection' in locals():
                db_connection.close()
                logging.info("Database connection closed cleanly.")
    else:
        logging.warning("Pipeline execution halted due to lack of source data.")
        
    logging.info("=== Data Pipeline Process Completed ===")
