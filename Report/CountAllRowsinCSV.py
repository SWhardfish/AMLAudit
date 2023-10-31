import csv
import os


def count_rows_in_csv(directory):
    total_rows = 0

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    rows_in_file = sum(1 for row in csv_reader)
                    total_rows += rows_in_file
            except Exception as e:
                print(f"Error reading file {filename}: {str(e)}")

    return total_rows


# Replace 'your_directory_path' with the actual directory path containing the CSV files
directory_path = '../BGMaxFiles/2023/Jan/PreProcessed'

total_rows = count_rows_in_csv(directory_path)
print(f"Total rows in all CSV files: {total_rows}")
