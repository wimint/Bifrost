import datetime
import pandas as pd
import re

# Read the 'usernames_uids_gids_2025_2_20.csv' file
usernames_df = pd.read_csv('usernames_uids_gids_2025_2_20.csv')

# Read the 'output_ukbb53639.csv' file
output_df = pd.read_csv('output_ukbb53639.csv')

# Create a dictionary for quick lookup of usernames by UID
uid_to_username = dict(zip(usernames_df.iloc[:, 1], usernames_df.iloc[:, 0]))

# Function to map clientUid_numerals to usernames
def map_uid_to_username(uid):
    return uid_to_username.get(uid, None)

# Apply the mapping function to the 'clientUid_numerals' column and create a new column
output_df['username'] = output_df['clientUid_numerals'].apply(map_uid_to_username)

# Save the updated DataFrame to a new CSV file
output_df.to_csv('output_ukbb53639_with_usernames.csv', index=False)

print("Conversion complete. The updated file is saved as 'output_ukbb53639_with_usernames.csv'.")