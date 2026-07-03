import os
import json
import pandas as pd
from datetime import datetime

print("Starting Silver layer transformation...")

# 1. Locate the Bronze data file dynamically based on today's date
today = datetime.now()
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")

bronze_file = os.path.join("storage", "bronze", f"year={year}", f"month={month}", f"day={day}", "raw_holidays.json")

# Safety Check: Does the Bronze file actually exist?
if not os.path.exists(bronze_file):
    print(f"Error: Could not find Bronze file at {bronze_file}. Run extract_holidays.py first!")
    exit()

# 2. Read the raw JSON file
with open(bronze_file, "r") as f:
    raw_data = json.load(f)

# 3. Load it into a Pandas DataFrame (a database-like table in memory)
df = pd.DataFrame(raw_data)

# 4. DATA CLEANING & TRANSFORMATION
# Let's clean up our columns to prepare for downstream analytics:
# - Rename columns to clean snake_case
# - Ensure dates are treated as actual Datetime objects
# - Convert that nested 'types' array into a clean comma-separated string
df = df.rename(columns={
    "date": "holiday_date",
    "localName": "local_name",
    "name": "english_name",
    "countryCode": "country_code",
    "launchYear": "launch_year"
})

# Cast string dates to true datetime types
df["holiday_date"] = pd.to_datetime(df["holiday_date"])

# Flatten the 'types' array: ['Public', 'Bank'] becomes 'Public, Bank'
df["types"] = df["types"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

# Drop columns we don't need for basic analysis
df = df.drop(columns=["counties"])

# 5. WRITE TO SILVER LAYER AS PARQUET
silver_dir = os.path.join("storage", "silver", "holidays")
os.makedirs(silver_dir, exist_ok=True)

silver_file = os.path.join(silver_dir, "clean_holidays.parquet")
df.to_parquet(silver_file, index=False)

print("Success!")
print(f"Silver Layer complete. Cleaned tabular data saved to Parquet format at: {silver_file}")
print("\nPeek at the transformed Silver table:")
print(df[["holiday_date", "local_name", "types"]].head())