import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load variables from the local .env file
load_dotenv()

print("Initializing connection to PostgreSQL...")

# 1. Locate and read our final Gold Parquet file
gold_file = os.path.join("storage", "gold", "long_weekends", "federal_long_weekends.parquet")

if not os.path.exists(gold_file):
    print(f"Error: Gold file not found at {gold_file}. Please run transform_gold.py first!")
    exit()

df = pd.read_parquet(gold_file)

# 2. Retrieve variables securely from the system environment
db_user = "postgres"
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = "localhost"
db_port = "5432"

# Construct the URL cleanly using string formatting
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL)

try:
    # 3. Stream the dataframe straight into a live database table
    print("Streaming Gold analytics tier to database...")
    df.to_sql("federal_long_weekends", engine, if_exists="replace", index=False)
    
    print("🎉 Success!")
    print(f"The table 'federal_long_weekends' is now live in your '{db_name}' database!")

except Exception as e:
    print("\n❌ Connection Error!")
    print(f"Could not connect to PostgreSQL. Technical details:\n{e}")