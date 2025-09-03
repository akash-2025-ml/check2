import pandas as pd
import numpy as np

# Read the Excel file
print("Reading 001.xlsx...")
df = pd.read_excel('001.xlsx')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Find the Data ID column (it might have different names)
data_id_col = None
for col in df.columns:
    if 'data' in col.lower() and 'id' in col.lower():
        data_id_col = col
        break
    elif col.lower() in ['id', 'data_id', 'email_id']:
        data_id_col = col
        break

if data_id_col is None:
    # If no Data ID column found, assume first column is the identifier
    data_id_col = df.columns[0]
    print(f"No Data ID column found, using first column: {data_id_col}")
else:
    print(f"Found Data ID column: {data_id_col}")

# Extract rows D71, D72, D73, D74, D75
target_ids = ['D71', 'D72', 'D73', 'D74', 'D75']

# Filter the dataframe for these IDs
extracted_data = df[df[data_id_col].isin(target_ids)]

print(f"\nFound {len(extracted_data)} rows matching D71-D75")
print("Matched IDs:", list(extracted_data[data_id_col]))

if len(extracted_data) == 0:
    print("No matching rows found. Let me check the actual values in the Data ID column:")
    print("Sample Data ID values:")
    print(df[data_id_col].head(10).tolist())
    print("...")
    print(df[data_id_col].tail(10).tolist())
    
    # Try to find rows that might be D71-D75 with different formatting
    print("\nSearching for rows containing '71', '72', '73', '74', '75':")
    for target in ['71', '72', '73', '74', '75']:
        matching_rows = df[df[data_id_col].astype(str).str.contains(target, na=False)]
        if not matching_rows.empty:
            print(f"Rows containing '{target}': {list(matching_rows[data_id_col])}")
else:
    # Save to CSV for easy viewing
    extracted_data.to_csv('extracted_D71_D75_data.csv', index=False)
    
    # Save to Excel as well
    extracted_data.to_excel('extracted_D71_D75_data.xlsx', index=False)
    
    # Display the data structure
    print(f"\nExtracted data shape: {extracted_data.shape}")
    print(f"Columns: {len(extracted_data.columns)} total")
    
    # Show first few columns to verify structure
    print("\nFirst few columns of extracted data:")
    print(extracted_data.iloc[:, :5])
    
    # Show column names to identify detection signals
    print(f"\nAll column names:")
    for i, col in enumerate(extracted_data.columns):
        print(f"{i+1}: {col}")
    
    print(f"\nData successfully extracted and saved to:")
    print("- extracted_D71_D75_data.csv")
    print("- extracted_D71_D75_data.xlsx")