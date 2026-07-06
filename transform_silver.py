import os
import duckdb

def run_silver_transformation():
    print("🚀 Starting DuckDB Silver Transformation...")
    
    # 1. Update this to your exact nested partition path
    bronze_path = "storage/bronze/year=2026/month=07/day=03/raw_holidays.json"
    
    # Target output folder and file matching your structure
    silver_dir = "storage/silver/holidays"
    silver_path = os.path.join(silver_dir, "clean_holidays.parquet")
    
    os.makedirs(silver_dir, exist_ok=True)
    
    # Initialize DuckDB session
    conn = duckdb.connect()
    
    # 2. Extract, clean, and cast directly from the raw partitioned JSON file
    query = f"""
        SELECT 
            CAST(date AS DATE) as holiday_date,
            CAST(localName AS VARCHAR) as local_name,
            CAST(name AS VARCHAR) as english_name,
            CAST(countryCode AS VARCHAR) as country_code,
            CAST(fixed AS BOOLEAN) as is_fixed,
            CAST(global AS BOOLEAN) as is_global
        FROM read_json_auto('{bronze_path}')
        WHERE date IS NOT NULL
    """
    
    print(f"🎬 Querying partitioned raw data from: {bronze_path}")
    
    # 3. Stream data directly from the JSON out to a Parquet file!
    conn.sql(query).write_parquet(silver_path)
    
    print(f"🎉 Success! Cleaned Silver file saved to: {silver_path}")
    
    # Let's peek at the newly created Parquet file using DuckDB SQL
    print("\n👀 First 5 rows of Silver Parquet layer:")
    print(conn.sql(f"SELECT * FROM read_parquet('{silver_path}') LIMIT 5").df())

if __name__ == "__main__":
    run_silver_transformation()