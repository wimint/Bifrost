import datetime
import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('dhukbb53639xggxe5eucentral1_DEC2024.csv')

# Function to convert Unix timestamp to human-readable date
def convert_timestamp(timestamp_ms):
    timestamp_s = timestamp_ms / 1000.0
    return datetime.datetime.fromtimestamp(timestamp_s).strftime('%Y-%m-%d %H:%M:%S')

# Function to extract numeral values from 'clientUid' field in 'message' column
def extract_numerals(message):
    match = re.search(r'"clientUid":"(\d+)"', message)
    return match.group(1) if match else None

# Apply the function to the first column and create a new column
df.insert(1, 'human_readable_timestamp', df.iloc[:, 0].apply(convert_timestamp))

# Apply the function to the 'message' column and create a new column
df['clientUid_numerals'] = df['message'].apply(extract_numerals)

# Save the updated DataFrame to a new CSV file
df.to_csv('output_ukbb53639.csv', index=False)

print("Conversion complete. The updated file is saved as 'output_ukbb53639.csv'.")