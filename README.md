# Automated Crypto Data Pipeline & REST API

A production-ready data engineering and backend project built with Python, SQLite, and FastAPI. It automatically extracts real-time market data from a public REST API, applies data transformations, utilizes secure parameter ingestion with rigorous error handling, and serves the dataset via scalable API endpoints.

## System Architecture

```text
 ┌──────────────────────┐
 │  CoinGecko REST API  │
 └──────────┬───────────┘
            │
            ▼ [Secure HTTP Fetch]
 ┌──────────────────────┐
 │     pipeline.py      │ ───► [Generates pipeline.log]
 └──────────┬───────────┘
            │
            ▼ [Parameterized SQL Ingestion]
 ┌──────────────────────┐
 │    market_data.db    │
 └──────────▲───────────┘
            │
            ▼ [SQLite Connection / Row Factory Mapping]
 ┌──────────────────────┐
 │        app.py        │ ◄──► [Uvicorn ASGI Server]
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │ http://localhost:8000│ ───► (/prices & /docs Swagger UI)
 └──────────────────────┘
