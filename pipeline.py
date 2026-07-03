import time
import logging
import requests
import sqlite3
from datetime import datetime

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

DB_NAME = "market_data.db"
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin_id TEXT NOT NULL,
            price_usd REAL NOT NULL,
            change_24h REAL,
            ingested_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def fetch_and_save_data():
    """Fetches real-time crypto data and logs it into the database."""
    logging.info("Starting automated data ingestion cycle...")
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        current_time = datetime.now().isoformat()
        
        for coin_id, metrics in data.items():
            price = metrics.get("usd")
            change = metrics.get("usd_24h_change")
            
            cursor.execute("""
                INSERT INTO crypto_prices (coin_id, price_usd, change_24h, ingested_at)
                VALUES (?, ?, ?, ?)
            """, (coin_id, price, change, current_time))
            
        conn.commit()
        conn.close()
        logging.info("Successfully ingested and saved market data for Bitcoin, Ethereum, and Solana.")
        
    except Exception as e:
        logging.error(f"Pipeline execution failed: {str(e)}")

def start_scheduler(interval_seconds=60):
    """Keeps the script running indefinitely, executing the pipeline at regular intervals."""
    init_db()
    logging.info(f"Crypto Data Pipeline Scheduler Activated. Running every {interval_seconds} seconds. Press CTRL+C to stop.")
    
    try:
        while True:
            fetch_and_save_data()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped manually by user. Shutting down cleanly.")

if __name__ == "__main__":
    # Runs the pipeline automatically every 60 seconds
    start_scheduler(interval_seconds=60)
