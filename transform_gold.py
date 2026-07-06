import os
import duckdb

def run_gold_transformation():
    print("✨ Starting DuckDB Gold Transformation...")
    
    # Paths matching your exact tree layout
    silver_path = "storage/silver/holidays/clean_holidays.parquet"
    gold_dir = "storage/gold/long_weekends"
    gold_path = os.path.join(gold_dir, "federal_long_weekends.parquet")
    
    os.makedirs(gold_dir, exist_ok=True)
    
    conn = duckdb.connect()
    
    # Write pure SQL to isolate federal long weekends
    # We read directly from the Parquet file as a table!
    query = f"""
        SELECT 
            holiday_date,
            local_name,
            english_name,
            country_code,
            -- Let's extract the day of the week to help verify long weekends
            strftime(holiday_date, '%A') as day_of_week
        FROM read_parquet('{silver_path}')
        WHERE is_global = true 
          AND country_code = 'US'
          -- Long weekends typically fall on Friday (5) or Monday (1)
          AND dayofweek(holiday_date) IN (1, 5)
        ORDER BY holiday_date ASC
    """
    
    print(f"🎬 Aggregating business metrics from Silver tier...")
    
    # Execute and stream straight out to your Gold Parquet layer
    conn.sql(query).write_parquet(gold_path)
    
    print(f"🏆 Success! Analytical Gold file saved to: {gold_path}")
    
    # Peek at the final golden data asset
    print("\n👀 Gold Layer Preview (Federal Long Weekends):")
    print(conn.sql(f"SELECT * FROM read_parquet('{gold_path}')").df())

if __name__ == "__main__":
    run_gold_transformation()