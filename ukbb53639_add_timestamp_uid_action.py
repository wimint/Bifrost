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

# Function to extract action values from 'operation' field in 'message' column
def extract_operation(message):
    match = re.search(r'"operation":"([^"]+)"', message)
    return match.group(1) if match else None

# Apply the function to the first column and create a new column
df.insert(1, 'human_readable_timestamp', df.iloc[:, 0].apply(convert_timestamp))

# Apply the function to the 'message' column and create a new column for clientUid
df['clientUid_numerals'] = df['message'].apply(extract_numerals)

# Apply the function to the 'message' column and create a new column for operation
df['operation'] = df['message'].apply(extract_operation)

# Save the updated DataFrame to a new CSV file
df.to_csv('output_ukbb53639_2.csv', index=False)

print("Conversion complete. The updated file is saved as 'output_ukbb53639_2.csv'.")

# Read the 'output_ukbb53639_2.csv' file
output_df = pd.read_csv('output_ukbb53639_2.csv')

# Read the 'data_dictionary.csv' file
data_dict_df = pd.read_csv('data_dictionary.csv')

# Create a dictionary for quick lookup of usernames by UID
uid_to_username = dict(zip(data_dict_df['userid'], data_dict_df['username']))

# Function to map clientUid_numerals to usernames
def map_uid_to_username(uid):
    return uid_to_username.get(uid, None)

# Apply the mapping function to the 'clientUid_numerals' column and create a new column
output_df['userid'] = output_df['clientUid_numerals'].apply(map_uid_to_username)

# Save the updated DataFrame to a new CSV file
output_df.to_csv('output_ukbb53639_with_usernames.csv', index=False)

print("Conversion complete. The updated file is saved as 'output_ukbb53639_with_usernames.csv',")
