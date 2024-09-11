import pandas as pd
import re
city = 'yenbai'
# Load the Excel file
file_path = city+'.xlsx'
df = pd.read_excel(file_path, sheet_name='Thống kê đề cập')

# Define regular expressions for detecting phone numbers and addresses
# Example for Vietnamese phone number pattern (based on common formats like 09xx xxx xxx or +84)
phone_pattern = r"(\+84|0)(\d{9,10})"
# Simplified address pattern (looking for common words used in addresses like "phường", "xã", "quận", "huyện", etc.)
address_pattern = r"(phường|xã|quận|huyện|thị trấn|tỉnh|thành phố|TP)\s\w+"

# Extract phone numbers and addresses using regex
df['Phone Numbers'] = df['Publish Content'].apply(lambda x: re.findall(phone_pattern, x))
df['Addresses'] = df['Publish Content'].apply(lambda x: re.findall(address_pattern, x))

# Filter rows that have either phone numbers or addresses
filtered_df = df[(df['Phone Numbers'].str.len() > 0) | (df['Addresses'].str.len() > 0)]

# Remove duplicate rows based on 'Phone Numbers' and 'Addresses'
# Converting lists to strings to make them hashable and comparable for deduplication
filtered_df['Phone Numbers'] = filtered_df['Phone Numbers'].apply(lambda x: ', '.join([''.join(num) for num in x]))
filtered_df['Addresses'] = filtered_df['Addresses'].apply(lambda x: ', '.join(x))

# Drop duplicate entries based on 'Phone Numbers' and 'Addresses'
deduplicated_df = filtered_df.drop_duplicates(subset=['Phone Numbers', 'Addresses'], keep='first')

columns_to_drop = ['Content Title','Data Source','Sentiment Category','Number of like','Number of comment','Number of share','Domain','author_url','Source Category','Unnamed: 13','Unnamed: 14','Unnamed: 15','Content Tags']
deduplicated_df_cleaned = deduplicated_df.drop(columns=columns_to_drop)

# Output the deduplicated DataFrame
print(deduplicated_df_cleaned[['Index Number', 'Publish Content', 'Phone Numbers', 'Addresses']])

# Save the deduplicated results to a new Excel file
deduplicated_df_cleaned.to_excel(city+'_results.xlsx', index=False)