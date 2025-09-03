#!/usr/bin/env python3
"""
Extract D96-D100 data from 001.xlsx
Final batch completing the analysis of all 100 emails
"""

import pandas as pd
import numpy as np

def extract_d96_d100_data():
    # Read the Excel file
    print("Reading 001.xlsx...")
    df = pd.read_excel('/home/u3/email_data/check2/001.xlsx')
    
    print(f"Total rows in dataset: {len(df)}")
    print(f"Total columns in dataset: {len(df.columns)}")
    print("\nColumn names:")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    # Extract rows D96-D100 (rows 95-99 in 0-based indexing)
    target_rows = df.iloc[95:100].copy()
    
    print(f"\nExtracted {len(target_rows)} rows (D96-D100)")
    
    # Save to CSV for analysis
    csv_path = '/home/u3/email_data/check2/extracted_D96_D100_data.csv'
    target_rows.to_csv(csv_path, index=False)
    print(f"Data saved to: {csv_path}")
    
    # Save to Excel as well
    excel_path = '/home/u3/email_data/check2/extracted_D96_D100_data.xlsx'
    target_rows.to_excel(excel_path, index=False)
    print(f"Data saved to: {excel_path}")
    
    # Display basic information about the extracted data
    print("\n" + "="*80)
    print("EXTRACTED DATA SUMMARY - D96 TO D100")
    print("="*80)
    
    # Check if Data ID column exists
    data_id_col = None
    for col in df.columns:
        if 'data' in col.lower() and 'id' in col.lower():
            data_id_col = col
            break
    
    if data_id_col:
        print(f"\nData IDs in extracted batch:")
        for idx, data_id in enumerate(target_rows[data_id_col]):
            print(f"Row {idx+96}: {data_id}")
    
    # Display the data structure
    print(f"\nDataset structure:")
    print(f"- Rows extracted: {len(target_rows)}")
    print(f"- Total columns: {len(target_rows.columns)}")
    
    # Show first few columns of extracted data
    print(f"\nFirst 10 columns preview:")
    preview_cols = target_rows.columns[:10]
    print(target_rows[preview_cols].to_string(index=False))
    
    # Count detection signals (assuming they are binary 0/1 values)
    numeric_cols = target_rows.select_dtypes(include=[np.number]).columns
    signal_cols = [col for col in numeric_cols if col != data_id_col]
    
    if signal_cols:
        print(f"\nDetection signals analysis:")
        print(f"- Total signal columns: {len(signal_cols)}")
        
        for idx, row_idx in enumerate(range(95, 100)):
            row_data = target_rows.iloc[idx]
            data_id = row_data[data_id_col] if data_id_col else f"D{row_idx+1}"
            
            # Count positive signals
            positive_signals = sum([1 for col in signal_cols if pd.notna(row_data[col]) and row_data[col] == 1])
            total_signals = len([col for col in signal_cols if pd.notna(row_data[col])])
            
            print(f"  {data_id}: {positive_signals}/{total_signals} signals triggered")
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    
    return target_rows

if __name__ == "__main__":
    extracted_data = extract_d96_d100_data()