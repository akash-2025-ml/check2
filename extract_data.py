import pandas as pd
import sys

def extract_email_data():
    """Extract D51-D55 rows from the Excel file with all signal columns"""
    
    try:
        # Read the Excel file
        df = pd.read_excel('001.xlsx')
        
        print(f"Excel file loaded successfully. Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few rows to understand the structure:")
        print(df.head())
        
        # Check if there's a Data ID column or similar identifier
        id_column = None
        for col in df.columns:
            if 'id' in col.lower() or 'data' in col.lower():
                id_column = col
                break
        
        if id_column is None:
            # If no ID column found, check if the first column contains the IDs
            if df.iloc[0:10, 0].astype(str).str.contains('D\d+').any():
                id_column = df.columns[0]
        
        print(f"\nUsing column '{id_column}' as identifier column")
        
        # Filter for D51-D55 rows
        target_ids = ['D51', 'D52', 'D53', 'D54', 'D55']
        
        if id_column:
            # Filter rows where the ID column contains our target IDs
            filtered_df = df[df[id_column].astype(str).isin(target_ids)]
        else:
            # If no clear ID column, try to find rows by searching all columns
            mask = df.astype(str).apply(lambda row: any(target_id in str(cell) for cell in row for target_id in target_ids), axis=1)
            filtered_df = df[mask]
        
        if filtered_df.empty:
            print("No rows found with IDs D51-D55. Let's examine the data structure more closely...")
            print("\nUnique values in first column:")
            print(df.iloc[:, 0].unique()[:20])  # Show first 20 unique values
            
            # Try alternative search approach
            for i, target_id in enumerate(target_ids):
                mask = df.astype(str).apply(lambda row: any(target_id in str(cell) for cell in row), axis=1)
                if mask.any():
                    print(f"Found {target_id} in row(s): {df.index[mask].tolist()}")
        else:
            print(f"\nFound {len(filtered_df)} rows matching D51-D55:")
            print(filtered_df)
            
            # Save to CSV for easy analysis
            output_file = 'extracted_D51_D55_data.csv'
            filtered_df.to_csv(output_file, index=False)
            print(f"\nData saved to: {output_file}")
            
            # Save to Excel as well
            output_excel = 'extracted_D51_D55_data.xlsx'
            filtered_df.to_excel(output_excel, index=False)
            print(f"Data also saved to: {output_excel}")
            
            # Show summary
            print(f"\nSummary:")
            print(f"- Extracted {len(filtered_df)} rows")
            print(f"- Total columns: {len(filtered_df.columns)}")
            print(f"- Column names: {list(filtered_df.columns)}")
            
            return filtered_df
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

if __name__ == "__main__":
    result = extract_email_data()