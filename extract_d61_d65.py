import pandas as pd
import sys

def extract_email_data():
    """Extract D61-D65 rows from the Excel file with all signal columns"""
    
    try:
        # Read the Excel file
        df = pd.read_excel('001.xlsx')
        
        print(f"Excel file loaded successfully. Shape: {df.shape}")
        print(f"Total columns: {len(df.columns)}")
        print(f"\nFirst 5 column names: {list(df.columns[:5])}")
        
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
        
        # Filter for D61-D65 rows
        target_ids = ['D61', 'D62', 'D63', 'D64', 'D65']
        
        if id_column:
            # Filter rows where the ID column contains our target IDs
            filtered_df = df[df[id_column].astype(str).isin(target_ids)]
        else:
            # If no clear ID column, try to find rows by searching all columns
            mask = df.astype(str).apply(lambda row: any(target_id in str(cell) for cell in row for target_id in target_ids), axis=1)
            filtered_df = df[mask]
        
        if filtered_df.empty:
            print("No rows found with IDs D61-D65. Let's examine the data structure more closely...")
            print("\nFirst 10 values in first column:")
            print(df.iloc[:10, 0].tolist())
            
            # Try alternative search approach - looking for numeric indices
            # D61 would be at index 60 (0-based indexing)
            indices = [60, 61, 62, 63, 64]  # D61-D65
            if max(indices) < len(df):
                print(f"\nTrying to extract by row indices {indices}...")
                filtered_df = df.iloc[indices]
                print(f"Successfully extracted {len(filtered_df)} rows by index")
        
        if not filtered_df.empty:
            print(f"\nFound {len(filtered_df)} rows:")
            print(f"Row indices: {filtered_df.index.tolist()}")
            
            # Save to CSV for easy analysis
            output_file = 'extracted_D61_D65_data.csv'
            filtered_df.to_csv(output_file, index=False)
            print(f"\nData saved to: {output_file}")
            
            # Save to Excel as well
            output_excel = 'extracted_D61_D65_data.xlsx'
            filtered_df.to_excel(output_excel, index=False)
            print(f"Data also saved to: {output_excel}")
            
            # Create a readable text report
            report_file = 'D61_D65_analysis_report.txt'
            with open(report_file, 'w') as f:
                f.write("Email Classification Data Analysis\n")
                f.write("=================================\n")
                f.write(f"Extracted data for emails: D61, D62, D63, D64, D65\n")
                f.write(f"Total detection signals: {len(filtered_df.columns) - 1}\n\n")
                
                # For each email
                for idx, row in filtered_df.iterrows():
                    f.write(f"\n{'='*60}\n")
                    f.write(f"Email ID: {row.iloc[0]}\n")
                    f.write(f"{'='*60}\n\n")
                    
                    # Group signals by their values for readability
                    active_signals = []
                    inactive_signals = []
                    
                    for col in filtered_df.columns[1:]:  # Skip the ID column
                        value = row[col]
                        if pd.notna(value) and value != 0:
                            active_signals.append((col, value))
                        else:
                            inactive_signals.append(col)
                    
                    f.write(f"Active Signals ({len(active_signals)}):\n")
                    f.write("-" * 40 + "\n")
                    for signal, value in sorted(active_signals):
                        f.write(f"  {signal}: {value}\n")
                    
                    f.write(f"\nInactive Signals ({len(inactive_signals)}):\n")
                    f.write("-" * 40 + "\n")
                    for i in range(0, len(inactive_signals), 3):
                        signals_chunk = inactive_signals[i:i+3]
                        f.write("  " + ", ".join(signals_chunk) + "\n")
            
            print(f"Readable report saved to: {report_file}")
            
            # Show summary
            print(f"\nSummary:")
            print(f"- Extracted {len(filtered_df)} rows")
            print(f"- Total columns: {len(filtered_df.columns)}")
            print(f"- Data ID column: {filtered_df.columns[0]}")
            print(f"- Signal columns: {len(filtered_df.columns) - 1}")
            
            return filtered_df
        else:
            print("Could not find the requested data rows.")
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = extract_email_data()