#directory_path = '../BGMAX PreProcess/BGMaxFiles/2023/Jan/PreProcessed'

import os

directory_path = "../BGMaxFiles/2023/Jan"

# Initialize counts for each pattern
pattern_counts = {"20": 0, "26": 0, "27": 0, "28": 0}

# Iterate over the files in the directory
for filename in os.listdir(directory_path):
    if os.path.isfile(os.path.join(directory_path, filename)):
        with open(os.path.join(directory_path, filename), 'r') as file:
            # Iterate over each line in the file
            for line in file:
                # Check if the first 2 characters match any of the specified patterns
                for pattern in pattern_counts.keys():
                    if line.strip().startswith(pattern):
                        pattern_counts[pattern] += 1

# Calculate the total count
total_count = sum(pattern_counts.values())

# Print the counts and total
for pattern, count in pattern_counts.items():
    print(f"Count for pattern '{pattern}': {count}")

print(f"Total count: {total_count}")
