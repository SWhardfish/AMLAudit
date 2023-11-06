import pandas as pd
from fuzzywuzzy import fuzz
import json
import os
from configparser import ConfigParser
import logging

# Configure the logging system
logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read config.ini file
config_object = ConfigParser()
config_object.read("../config.ini")

# Get the MonthYear
monthyear = config_object["MonthYear"]
year = monthyear["year"]
month = monthyear["month"]

output_dir = f'../BGMaxFiles/{year}/{month}/Matched/'

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)


# Iterate over each JSON file in '../PreProcessed/'
directory_path = f'../BGMaxFiles/{year}/{month}/Preprocessed/InvoiceProcessed/'
# Ensure output directories exist
os.makedirs(output_dir, exist_ok=True)
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        # Create an empty list to store data for the CSV for each file
        csv_data = []
        with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        header = data.get('header', {})
        payments = data.get('payments', [])

        # Read 'Date' field from the JSON data
        date = header.get('Date', "")

        file2_df = pd.read_csv('../FF9SECustomers/25Oct/FF9SECustomersCOL.csv', sep=';')

        # Join address fields into one
        file2_df["FFNameAddress"] = file2_df["Name"] + ',' + file2_df["Address"] + ' ' + file2_df["Post Code"] + ' ' + \
                                    file2_df["City"]
        file2_df["FFName"] = file2_df["Name"]
        file2_df["FFAddress"] = file2_df["Address"] + ' ' + file2_df["Post Code"] + ' ' + file2_df["City"]

        # Iterate over payments in the JSON data
        for payment in payments:
            Id = payment.get("id", )
            PaymentRecord = payment.get("PaymentRecord(20)", {})
            CustomerNo = PaymentRecord.get("CustomerNo", "NotFound")
            Amount = PaymentRecord.get("Amount", "")
            CompanyNumber = payment.get("CompanyNumber", "")
            Name = payment.get("Name", "")
            Address = payment.get("Address", "")
            City = payment.get("City", "")
            BGMaxNameAddress = f"{Name}, {Address} {City}"
            BGMaxAddress = f"{Address} {City}"

            if CompanyNumber:
                matching_row = file2_df[file2_df['VAT Registration No_'] == CompanyNumber]
                if not matching_row.empty:
                    FFNameAddress = matching_row.iloc[0]['FFNameAddress']
                    FFName = matching_row.iloc[0]['FFName']
                    FFAddress = matching_row.iloc[0]['FFAddress']

                    similarity = "100"  # Set the similarity to "100" when CompanyNumber matches
                    similarity_name = "100"  # Set the similarity to "100" when CompanyNumber matches
                    similarity_address = "100"  # Set the similarity to "100" when CompanyNumber matches
                    CustomerNo = CompanyNumber  # Set CustomerNo to CompanyNumber when there's a match
                else:
                    # No match found for CompanyNumber, so check 'No_'
                    matching_row = file2_df[file2_df['No_'] == CustomerNo]
                    if not matching_row.empty:
                        FFNameAddress = matching_row.iloc[0]['FFNameAddress']
                        FFName = matching_row.iloc[0]['FFName']
                        FFAddress = matching_row.iloc[0]['FFAddress']
                        similarity = fuzz.token_set_ratio(BGMaxNameAddress, FFNameAddress)
                        similarity_name = fuzz.token_set_ratio(Name, FFName)
                        similarity_address = fuzz.token_set_ratio(BGMaxAddress, FFAddress)
                    else:
                        FFNameAddress = f'No CustomerNumber {CustomerNo} match in FF9 Customer Table'
                        similarity = 0
                        similarity_name = 0
                        similarity_address = 0
                        # Log the information
                        logging.info(f"No CustomerNumber match for {CustomerNo} in {filename}")
            else:
                # CompanyNumber is empty, so check 'No_'
                matching_row = file2_df[file2_df['No_'] == CustomerNo]
                if not matching_row.empty:
                    FFNameAddress = matching_row.iloc[0]['FFNameAddress']
                    FFName = matching_row.iloc[0]['FFName']
                    FFAddress = matching_row.iloc[0]['FFAddress']
                    similarity = fuzz.token_set_ratio(BGMaxNameAddress, FFNameAddress)
                    similarity_name = fuzz.token_set_ratio(Name, FFName)
                    similarity_address = fuzz.token_set_ratio(BGMaxAddress, FFAddress)
                else:
                    FFNameAddress = f'No CustomerNumber {CustomerNo} match in FF9 Customer Table'
                    similarity = 0
                    similarity_name = 0
                    similarity_address = 0
                    # Log the information
                    logging.info(f"No CustomerNumber match for {CustomerNo} in {filename}")

            #Correct the Amount value- to remove the last two 00.
            try:
                Amount = int(Amount) / 100
            except ValueError:
                Amount = None  # You can set it to a default value or handle it in another way if needed

            # Append data to the CSV format
            csv_data.append([CustomerNo, date, Id, BGMaxNameAddress, Amount, FFNameAddress, similarity, similarity_name, similarity_address])

        # Write the data to a CSV file
        output_filename = f'../BGMaxFiles/{year}/{month}/Matched/{os.path.splitext(os.path.basename(filename))[0]}_output.csv'
        df = pd.DataFrame(csv_data, columns=["CustomerNo", "Date", "Id", "BGMaxNameAddress", "Amount", "FFNameAddress", "similarity", "similarity_name", "similarity_address"])
        df.to_csv(output_filename, index=False)
