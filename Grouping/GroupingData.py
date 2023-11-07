import os
import pandas as pd

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# Define the directories where your CSV files are located
directories = [
    '../BGMaxFiles/2022/Jan/Matched',
    '../BGMaxFiles/2022/Feb/Matched',
    '../BGMaxFiles/2022/Mar/Matched',
    '../BGMaxFiles/2022/Apr/Matched',
    '../BGMaxFiles/2022/May/Matched',
    '../BGMaxFiles/2022/Jun/Matched',
    '../BGMaxFiles/2022/Jul/Matched',
    '../BGMaxFiles/2022/Aug/Matched',
    '../BGMaxFiles/2022/Sep/Matched',
    '../BGMaxFiles/2022/Oct/Matched',
    '../BGMaxFiles/2022/Nov/Matched',
    '../BGMaxFiles/2022/Dec/Matched',
    '../BGMaxFiles/2023/Jan/Matched',
    '../BGMaxFiles/2023/Feb/Matched',
    '../BGMaxFiles/2023/Mar/Matched',
    '../BGMaxFiles/2023/Apr/Matched',
    '../BGMaxFiles/2023/May/Matched',
    '../BGMaxFiles/2023/Jun/Matched',
    '../BGMaxFiles/2023/Jul/Matched',
    '../BGMaxFiles/2023/Aug/Matched',
    '../BGMaxFiles/2023/Sep/Matched'
    #'../BGMaxFiles/2023/Oct/Matched',
    #'../BGMaxFiles/2023/Nov/Matched',
    #'../BGMaxFiles/2023/Dec/Matched',
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
#print(sorted_data)

# Save the sorted data to an Excel file
sorted_data.to_excel('sorted_data2022Jan-2023Sep.xlsx', index=False)
#print(sorted_data)
