# 2026 US Public Holidays Medallion Data Pipeline

An end-to-end data engineering pipeline implementing the **Medallion Architecture** (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) to extract public holiday data, transform it into highly optimized columnar storage, and model it for downstream business analytics.

## 🛠️ Architecture Overview

The project processes data through three distinct functional tiers inside a localized data lake structure:

1. **Bronze Layer (Ingestion):** Extracts raw JSON records dynamically from the Nager.at Public Holidays API and dumps them completely unaltered into date-partitioned storage (`year=YYYY/month=MM/day=DD/`) mimicking cloud blob storage Hive structures.
2. **Silver Layer (Transformation):** Reads the raw JSON, standardizes schemas into clean `snake_case`, handles type-casting of date strings into robust datetime objects, flattens semi-structured array fields, and drops non-critical columns. Saved as compressed **Parquet**.
3. **Gold Layer (Analytics Modeling):** Curates a specialized business layer table filtering out regional closures to map global/federal holidays, computes days of the week, and derives a boolean engine flag to identify 3-day holiday weekend planning opportunities.

---

## 📂 Data Lake Directory Structure

Because of data compliance and cost engineering best practices, raw and processed data assets are localized on the execution system and explicitly decoupled from source control via `.gitignore`. 

```text
storage/
├── bronze/
│   └── year=2026/
│       └── month=07/
│           └── day=03/
│               └── raw_holidays.json       # Raw API payload
├── silver/
│   └── holidays/
│       └── clean_holidays.parquet          # Columnar, clean schema
└── gold/
    └── long_weekends/
        └── federal_long_weekends.parquet   # High-value analytical model