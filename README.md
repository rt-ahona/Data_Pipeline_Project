# Automated Crypto Data Pipeline & REST API

A production-ready data engineering and backend project built with Python, SQLite, and FastAPI. It automatically extracts real-time market data from a public REST API, applies data transformations, secure parameter ingestion, error handling, and serves the dataset via scalable API endpoints.

## Features
- **Data Ingestion Script:** Fetches real-time structured marketplace metrics cleanly using network timeout metrics.
- **Data Integrity Layer:** Protects against SQL Injection attacks using parameterized querying into a relational SQLite schema.
- **Robust System Logging:** Implements file-audited structural execution history tracking.
- **Web Interface Endpoint:** Exposes interactive auto-generated Swagger UI routing via a lightweight FastAPI server core.

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install requests fastapi uvicorn
