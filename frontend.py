import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configure page styling
st.set_page_config(
    page_title="Crypto Market Data Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Real-Time Crypto Data Pipeline Dashboard")
st.markdown("This dashboard displays live cryptocurrency metrics fetched directly from our custom FastAPI backend application.")

# Backend API Endpoint URL
API_URL = "http://127.0.0.1:8000/prices"

# Add a refresh button in the UI
if st.button("🔄 Refresh Live Data"):
    st.rerun()

try:
    # Fetch data from our FastAPI server
    response = requests.get(API_URL, timeout=5)
    
    if response.status_code == 200:
        json_data = response.json()
        raw_records = json_data.get("data", [])
        
        if raw_records:
            # Convert raw JSON data into a structured Pandas DataFrame
            df = pd.DataFrame(raw_records)
            
            # Clean up names for display
            df['coin_id'] = df['coin_id'].str.capitalize()
            df['ingested_at'] = pd.to_datetime(df['ingested_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # 1. Metric Cards (KPI Highlights for latest entries)
            st.subheader("💡 Current Asset Status")
            col1, col2, col3 = st.columns(3)
            
            # Extract latest price points for metrics
            latest_data = df.drop_duplicates(subset=['coin_id'], keep='first')
            
            with col1:
                btc = latest_data[latest_data['coin_id'] == 'Bitcoin']
                if not btc.empty:
                    st.metric("Bitcoin (BTC)", f"${btc['price_usd'].values[0]:,}", f"{btc['change_24h'].values[0]:.2f}%")
            with col2:
                eth = latest_data[latest_data['coin_id'] == 'Ethereum']
                if not eth.empty:
                    st.metric("Ethereum (ETH)", f"${eth['price_usd'].values[0]:,}", f"{eth['change_24h'].values[0]:.2f}%")
            with col3:
                sol = latest_data[latest_data['coin_id'] == 'Solana']
                if not sol.empty:
                    st.metric("Solana (SOL)", f"${sol['price_usd'].values[0]:,}", f"{sol['change_24h'].values[0]:.2f}%")
            
            st.markdown("---")
            
            # 2. Visual Graphs Layout
            st.subheader("📈 Historical Ingestion Analytics")
            
            # Create a clean time-series trend line using Plotly
            fig = px.line(
                df, 
                x="ingested_at", 
                y="price_usd", 
                color="coin_id",
                labels={"ingested_at": "Timestamp", "price_usd": "Price (USD)", "coin_id": "Asset"},
                title="Price Movement Over Time (Database Ingestion Logs)"
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            
            # 3. Clean Structured Data Table View
            st.subheader("📁 Raw Database Records")
            st.dataframe(
                df[['id', 'coin_id', 'price_usd', 'change_24h', 'ingested_at']], 
                use_container_width=True
            )
            
        else:
            st.warning("The database is currently empty. Run your automated pipeline script to start collecting market records.")
            
    else:
        st.error(f"Could not connect to API server. Status Code: {response.status_code}")

except requests.exceptions.ConnectionError:
    st.error("🔌 Connection Error: Make sure your FastAPI backend app server is running on http://127.0.0.1:8000 before opening this dashboard!")