import os
import pandas as pd

print("Starting Gold layer aggregation...")

# 1. Locate and read the Silver Parquet file directly
silver_file = os.path.join("storage", "silver", "holidays", "clean_holidays.parquet")

if not os.path.exists(silver_file):
    print(f"Error: Silver file not found at {silver_file}. Please run transform_silver.py first!")
    exit()

df = pd.read_parquet(silver_file)

# 2. FILTER: Keep only global/national public holidays
# (Filtering out any state-specific bank or local closures)
gold_df = df[df["global"] == True].copy()

# 3. COMPUTE: Extract the day of the week from our true Datetime column
# This creates a readable string like 'Monday', 'Friday', etc.
gold_df["day_of_week"] = gold_df["holiday_date"].dt.day_name()

# 4. ANALYZE: Identify 3-Day Weekend Opportunities
# A holiday creates a long weekend if it falls on a Friday or a Monday!
gold_df["is_long_weekend"] = gold_df["day_of_week"].isin(["Friday", "Monday"])

# 5. SELECT & REORDER: Streamline down to only business-critical columns
gold_columns = ["holiday_date", "english_name", "day_of_week", "is_long_weekend"]
gold_df = gold_df[gold_columns]

# 6. WRITE TO GOLD LAYER AS PARQUET
gold_dir = os.path.join("storage", "gold", "long_weekends")
os.makedirs(gold_dir, exist_ok=True)

gold_file = os.path.join(gold_dir, "federal_long_weekends.parquet")
gold_df.to_parquet(gold_file, index=False)

print("Success!")
print(f"Gold Layer complete. Specialized analytics table saved to: {gold_file}")