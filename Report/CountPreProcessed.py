import os

# Directory to count rows
preprocessed_directory = "../BGMaxFiles/2023/Jan/PreProcessed"

# Initialize counts for each pattern
pattern_counts_additional = {"Complete with Customer Number": 0, "Incomplete missing Customer Number": 0}

# Function to count rows based on patterns
def count_rows(file_path):
    start_with_number_pattern = "^(\d+),"
    start_with_empty_pattern = "^,(\d+),"

    with open(file_path, 'r', encoding="utf8") as file:
        # Skip the header line
        next(file)
        # Iterate over each line in the file
        for line in file:
            if line.strip() == '':
                continue  # Skip empty lines
            # Check if the line matches start_with_number pattern
            if line.strip().startswith(tuple(str(i) for i in range(10))):
                pattern_counts_additional["Complete with Customer Number"] += 1
            # Check if the line matches start_with_empty pattern
            elif line.strip().startswith(','):
                pattern_counts_additional["Incomplete missing Customer Number"] += 1

# Iterate over the files in the additional directory
for filename in os.listdir(preprocessed_directory):
    if os.path.isfile(os.path.join(preprocessed_directory, filename)):
        count_rows(os.path.join(preprocessed_directory, filename))

# Print the counts for the additional directory
for pattern, count in pattern_counts_additional.items():
    print(f"Count Preprocessed records '{pattern}': {count}")

# Calculate the total count for the additional directory
total_count_additional = sum(pattern_counts_additional.values())

print(f"Total count for Preprocessed directory: {total_count_additional}")
