import csv

whitelist_data = {}
output_data = []

# Step 1: Read whitelist.csv and store data in a dictionary
with open('whitelist.csv', 'r', newline='', encoding='utf-8') as whitelist_file:
    whitelist_reader = csv.DictReader(whitelist_file)
    for row in whitelist_reader:
        customer_no = int(row['CustomerNo'])
        name_address = row['NameAddress'].strip()
        whitelist_data[customer_no] = name_address

# Step 2: Read output.csv, perform comparisons, and update the data
with open('output.csv', 'r', newline='', encoding='utf-8') as output_file:
    output_reader = csv.DictReader(output_file)
    for row in output_reader:
        customer_no = int(row['CustomerNo'])
        name_address = row['NameAddress'].strip()
        ff_name_address = row['FFNameAddress'].strip()

        if customer_no in whitelist_data and whitelist_data[customer_no] == name_address:
            row['Whitelist'] = 'Yes'
        else:
            row['Whitelist'] = 'No'

        output_data.append(row)

# Step 3: Write updated data to outputw.csv
header = ['CustomerNo', 'NameAddress', 'FFNameAddress', 'similarity', 'Whitelist']

with open('outputw.csv', 'w', newline='') as outputw_file:
    writer = csv.DictWriter(outputw_file, fieldnames=header)
    writer.writeheader()
    for row in output_data:
        writer.writerow(row)
