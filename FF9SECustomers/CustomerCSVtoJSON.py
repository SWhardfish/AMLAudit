import pandas as pd

# Replace 'your_file.csv' with the actual CSV file name
csv_file = 'FF9SEcustomers.csv'

# Read the CSV file
df = pd.read_csv(csv_file, sep=';', encoding='utf-8')

# Drop the 'timestamp' column
df = df.drop(columns=['timestamp'])

# Convert the DataFrame to JSON
json_data = df.to_json(orient='records', default_handler=str)

# Define the output JSON file name
json_file = csv_file.replace('.csv', '.json')

# Write the JSON data to a new file with the same name as the original CSV file
with open(json_file, 'w') as file:
    file.write(json_data)

print(f'CSV file "{csv_file}" has been converted to JSON and saved as "{json_file}"')
