import os
import sqlite3
import pandas as pd
from datetime import datetime

# Create an SQLite database and a table to store the CSV data
conn = sqlite3.connect("csv_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_record (
    CustomerNo INTEGER,
    Date TEXT,
    NameAddress TEXT,
    FFNameAddress TEXT,
    Similarity INTEGER,
    Status TEXT,
    UnderReview TEXT,
    Timestamp DATETIME,
    UserAudit TEXT,
    Comment TEXT
);
""")
conn.commit()

# Define the directories where the CSV files are located
directories = [
    '../BGMaxFiles/2023/Jan/Matched',
    '../BGMaxFiles/2023/Feb/Matched'
]

# Function to read and import CSV files into the SQLite database
def import_csv_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path, quotechar='"', escapechar='\\')
                # Add empty columns for the new fields
                df['Status'] = ''
                df['UnderReview'] = ''
                df['Timestamp'] = None
                df['UserAudit'] = ''
                df['Comment'] = ''
                df.to_sql('customer_record', conn, if_exists='append', index=False)

# Loop through the directories and import CSV data
for directory in directories:
    import_csv_files(directory)

# Close the database connection
conn.close()
