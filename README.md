# Automated Crypto Data Pipeline & Full-Stack REST Dashboard

A production-ready, full-stack data engineering and analytics application built with Python, SQLite, FastAPI, and Streamlit. The system automatically extracts real-time market data from a public REST API via an autonomous scheduler, applies data transformations, safeguards persistence using parameterized SQL queries, and serves the database via a scalable REST API alongside an interactive data visualization dashboard.

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
 │        app.py        │ ◄──► [FastAPI / Uvicorn REST API]
 └──────────▲───────────┘
            │
            ▼ [JSON Serialization Layer]
 ┌──────────────────────┐
 │     frontend.py      │ ◄──► [Streamlit UI Dashboard]
 └──────────────────────┘