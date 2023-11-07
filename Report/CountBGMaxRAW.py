import os
import matplotlib.pyplot as plt
import seaborn as sns

# List of directories to process
directories = [
    '../BGMaxFiles/2022/Jan/',
    '../BGMaxFiles/2022/Feb/',
    '../BGMaxFiles/2022/Mar/',
    '../BGMaxFiles/2022/Apr/',
    '../BGMaxFiles/2022/May/',
    '../BGMaxFiles/2022/Jun/',
    '../BGMaxFiles/2022/Jul/',
    '../BGMaxFiles/2022/Aug/',
    '../BGMaxFiles/2022/Sep/',
    '../BGMaxFiles/2022/Oct/',
    '../BGMaxFiles/2022/Nov/',
    '../BGMaxFiles/2022/Dec/',
    '../BGMaxFiles/2023/Jan/',
    '../BGMaxFiles/2023/Feb/',
    '../BGMaxFiles/2023/Mar/',
    '../BGMaxFiles/2023/Apr/',
    '../BGMaxFiles/2023/May/',
    '../BGMaxFiles/2023/Jun/',
    '../BGMaxFiles/2023/Jul/',
    '../BGMaxFiles/2023/Aug/',
    '../BGMaxFiles/2023/Sep/'
]

# Initialize counts for each pattern
pattern_counts = {"20": 0, "26": 0, "27": 0, "28": 0}

# Iterate over the directories
for directory_path in directories:
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
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

# Create a bar chart using Seaborn
patterns = pattern_counts.keys()
counts = pattern_counts.values()

sns.set(style="whitegrid")  # Set the style
plt.figure(figsize=(7, 5))  # Set the figure size

# Create a barplot using Seaborn
ax = sns.barplot(x=list(patterns), y=list(counts), width=0.2, legend="auto", palette="Set3")
ax.set(xlabel='BGMax Row Types', ylabel='Counts')
plt.title('Row counts in the BGMax Files 2022-2023(Sep)')

# Annotate each bar with its count
for pattern, count in zip(patterns, counts):
    ax.text(pattern, count, str(count), ha='center', va='bottom', size=10)

plt.show()
