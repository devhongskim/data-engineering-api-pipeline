import requests
import json
import os
from datetime import datetime

URL = "https://date.nager.at/api/v3/PublicHolidays/2026/US"

print("Starting API extraction...")

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    holiday_data = response.json()
    print(f"Success! Extracted {len(holiday_data)} holidays.")
    
    # --- BRONZE LANDING ZONE STRATEGY ---
    # 1. Get today's date dynamically to build Hive partitions
    today = datetime.now()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    
    # 2. Define our Bronze structure path: bronze/year=YYYY/month=MM/day=DD/
    # This structure protects us from scanning the entire collection of data later!
    bronze_dir = os.path.join("storage", "bronze", f"year={year}", f"month={month}", f"day={day}")
    
    # 3. Create the directories if they don't exist yet
    os.makedirs(bronze_dir, exist_ok=True)
    
    # 4. Define the file name and full path
    file_path = os.path.join(bronze_dir, "raw_holidays.json")
    
    # 5. Write the raw untouched JSON to disk
    with open(file_path, "w") as f:
        json.dump(holiday_data, f, indent=4)
        
    print(f"Bronze Layer Success: Raw data landed safely at: {file_path}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Network Connection Error occurred: {conn_err}")
except Exception as err:
    print(f"An unexpected error occurred: {err}")