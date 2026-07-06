# Production-Grade Medallion Data Pipeline (DuckDB + PostgreSQL)

An automated data engineering pipeline that extracts international holiday data from a third-party REST API, processes it through a local three-tiered data lake (Medallion Architecture), and loads the optimized analytical tier into a PostgreSQL relational database.

## 🏗️ Architecture Overview

The system is designed around modern data engineering principles, separating the storage/processing layer from the active query/serving layer.
```
[REST API] ──> [Bronze Layer] ───> [Silver Layer] ───> [Gold Layer] ───> [PostgreSQL]
(Nager.Date)    (Raw JSON,      (Clean Parquet)    (Aggregated     (Data Mart for
               Partitioned)                        Parquet)        Applications)
                    │                  │                  │              │
                    └──────────────────┴─────────┬────────┴──────────────┘
                                         Engine: DuckDB SQL
```

* **Extraction (Bronze):** Ingests raw JSON payloads from the API and structures them into a time-partitioned directory layout (year=YYYY/month=MM/day=DD) mimicking cloud blob storage Hive structures to preserve historical raw data immutability.
* **Transformation (Silver):** Leverages DuckDB to execute zero-server in-memory SQL directly on the raw nested JSON, casting explicit data types, standardizing schemas into snake_case, and saving the output as highly compressed Parquet files.
* **Analytics Tier (Gold):** Filters and aggregates the data using columnar DuckDB SQL logic to produce business-ready data structures, computing days of the week and identifying 3-day federal holiday weekend planning opportunities.
* **Serving Layer (PostgreSQL):** Streams the Gold tier datasets into a PostgreSQL instance using SQLAlchemy, serving as a clean relational data mart ready for downstream BI tools or enterprise applications.

---

## 🛠️ Tech Stack & Key Design Patterns

* **Language:** Python 3.11+
* **OLAP Query Engine:** DuckDB (Chosen over Pandas for vectorized, memory-efficient columnar processing and direct-to-file SQL querying capabilities).
* **Storage Tier:** Apache Parquet (Provides optimal disk-compression and fast column scanning speeds).
* **Relational Database:** PostgreSQL (Connected securely via SQLAlchemy/Psycopg2).
* **Environment Management:** Separated secrets (.env) from configuration, fully controlled tracking patterns (.gitignore).

---

## 📂 Data Lake Directory Structure

Because of data compliance and cost engineering best practices, raw and processed data assets are localized on the execution system and explicitly decoupled from source control via .gitignore.
```
storage/
├── bronze/
│   └── year=2026/
│       └── month=07/
│           └── day=03/
│               └── raw_holidays.json       # Raw API payload
├── silver/
│   └── holidays/
│       └── clean_holidays.parquet          # Columnar, clean schema via DuckDB
└── gold/
    └── long_weekends/
        └── federal_long_weekends.parquet   # High-value analytical model via DuckDB
```
---

## ⚙️ Setup and Installation

### Prerequisites
* Python 3.11+
* A running instance of PostgreSQL

### 1. Clone the Repository
git clone [https://github.com/YOUR_USERNAME/data-engineering-api-pipeline.git](https://github.com/YOUR_USERNAME/data-engineering-api-pipeline.git)
cd data-engineering-api-pipeline

### 2. Install Dependencies
pip install duckdb sqlalchemy psycopg2-binary requests python-dotenv pandas

### 3. Configure Your Environment Variables
Create a .env file in the project root directory and supply your database credentials:

DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=holiday_pipeline

---

## 🚀 Running the Pipeline

The pipeline runs sequentially to move and transform data from the source out to production:

# Phase 1: Extract API data to Partitioned Bronze Layer
python extract_holidays.py

# Phase 2: Refactor and clean data to Silver Parquet Layer using DuckDB
python transform_silver.py

# Phase 3: Build analytical business views into Gold Parquet Layer
python transform_gold.py

# Phase 4: Stream analytical Gold layer into PostgreSQL Production
python load_gold_to_postgres.py

---

## 📊 Evolutionary Log (Portfolio Milestone)

* **V1.0 (Functional Prototype):** Initially built the pipeline utilizing Pandas for standard manipulation and storage as flat CSVs.
* **V2.0 (Architectural Optimization):** Refactored the core transformations to use DuckDB. Replaced implicit python logic with structured SQL operations and switched storage types to Apache Parquet, achieving significantly reduced RAM usage and executing transformations up to 10x faster on disk records.
