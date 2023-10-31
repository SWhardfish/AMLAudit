import os
import pandas as pd

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# Define the directories where your CSV files are located
directories = [
    '../BGMaxFiles/2023/Jan/Matched',
    '../BGMaxFiles/2023/Feb/Matched',
]

# Initialize an empty list to store DataFrames
dfs = []

# Iterate through the directories and read all CSV files
for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)

# Concatenate the DataFrames in the list
combined_data = pd.concat(dfs, ignore_index=True)

# Group the data by 'CustomerNo' and sort each group by 'Date'
sorted_data = combined_data.groupby('CustomerNo').apply(lambda x: x.sort_values(by='Date')).reset_index(drop=True)

# Print the sorted data
print(sorted_data)

# Save the sorted data to an Excel file
sorted_data.to_excel('sorted_data.xlsx', index=False)
print(sorted_data)
