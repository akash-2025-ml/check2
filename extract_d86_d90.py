#!/usr/bin/env python3
"""
Extract data for D86-D90 from 001.xlsx
"""

import pandas as pd
import sys

def extract_d86_d90():
    try:
        # Read the Excel file
        print("Reading 001.xlsx...")
        df = pd.read_excel('001.xlsx')
        
        print(f"File shape: {df.shape}")
        print(f"Total columns: {len(df.columns)}")
        
        # Get the Data ID column name (first column)
        data_id_col = df.columns[0]
        print(f"Data ID column: '{data_id_col}'")
        
        # Filter for D86-D90 rows
        target_ids = ['D86', 'D87', 'D88', 'D89', 'D90']
        filtered_df = df[df[data_id_col].isin(target_ids)]
        
        if len(filtered_df) == 0:
            print("ERROR: No rows found for D86-D90")
            return False
            
        print(f"Found {len(filtered_df)} rows for D86-D90")
        
        # Sort by Data ID to ensure proper order
        filtered_df = filtered_df.sort_values(by=data_id_col)
        
        # Save to CSV for analysis
        csv_filename = 'extracted_D86_D90_data.csv'
        filtered_df.to_csv(csv_filename, index=False)
        print(f"Saved to: {csv_filename}")
        
        # Save to Excel as well
        excel_filename = 'extracted_D86_D90_data.xlsx'
        filtered_df.to_excel(excel_filename, index=False)
        print(f"Saved to: {excel_filename}")
        
        # Display the extracted data
        print("\n" + "="*80)
        print("EXTRACTED DATA FOR D86-D90:")
        print("="*80)
        
        # Show basic info
        print(f"Data shape: {filtered_df.shape}")
        print(f"Columns: {len(filtered_df.columns)} (1 Data ID + {len(filtered_df.columns)-1} detection signals)")
        
        # Display the data in a readable format
        print("\nData Overview:")
        for idx, row in filtered_df.iterrows():
            data_id = row[data_id_col]
            print(f"\n{data_id}:")
            
            # Show non-zero signal values for each email
            non_zero_signals = []
            for col in filtered_df.columns[1:]:  # Skip Data ID column
                if pd.notna(row[col]) and row[col] != 0:
                    non_zero_signals.append(f"{col}: {row[col]}")
            
            if non_zero_signals:
                for signal in non_zero_signals[:10]:  # Show first 10 non-zero signals
                    print(f"  {signal}")
                if len(non_zero_signals) > 10:
                    print(f"  ... and {len(non_zero_signals) - 10} more non-zero signals")
            else:
                print("  All signals are 0 or null")
        
        # Create a summary table
        print("\n" + "="*80)
        print("SUMMARY TABLE:")
        print("="*80)
        
        # Show all data in a transposed format for better readability
        transposed_df = filtered_df.set_index(data_id_col).T
        
        # Show first 20 detection signals
        print("\nFirst 20 Detection Signals:")
        print(transposed_df.head(20).to_string())
        
        # Count non-zero signals per email
        print("\n" + "="*80)
        print("SIGNAL ACTIVITY SUMMARY:")
        print("="*80)
        
        for data_id in target_ids:
            if data_id in filtered_df[data_id_col].values:
                row_data = filtered_df[filtered_df[data_id_col] == data_id].iloc[0]
                non_zero_count = sum(1 for val in row_data[1:] if pd.notna(val) and val != 0)
                total_signals = len(row_data) - 1
                print(f"{data_id}: {non_zero_count}/{total_signals} signals active ({non_zero_count/total_signals*100:.1f}%)")
            else:
                print(f"{data_id}: NOT FOUND")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = extract_d86_d90()
    sys.exit(0 if success else 1)