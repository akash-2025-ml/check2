#!/usr/bin/env python3
import pandas as pd

def analyze_d76_d80():
    """Analyze the extracted D76-D80 email data"""
    
    # Read the extracted data
    df = pd.read_csv('/home/u3/email_data/check2/extracted_D76_D80_data.csv')
    
    print('=== EMAIL DATA ANALYSIS: D76-D80 ===')
    print(f'Total emails: {len(df)}')
    print(f'Total detection signals: {len(df.columns)-1}')  # Minus the Data ID column
    print()
    
    # Analyze each email
    for idx, row in df.iterrows():
        data_id = row['Data ']
        print(f'--- {data_id} ---')
        
        # Count non-zero signals
        signal_cols = df.columns[1:]  # All columns except Data ID
        active_signals = []
        signal_values = []
        
        for col in signal_cols:
            if pd.notna(row[col]) and row[col] != 0:
                active_signals.append(col)
                signal_values.append(row[col])
        
        print(f'Active signals: {len(active_signals)} out of {len(signal_cols)}')
        
        if active_signals:
            print('Active signals and their values:')
            for signal, value in zip(active_signals, signal_values):
                print(f'  {signal}: {value}')
        else:
            print('No active signals detected')
        print()
    
    # Create a summary report
    print('=== SUMMARY REPORT ===')
    report_lines = []
    report_lines.append('EMAIL DATA EXTRACTION REPORT - D76 to D80')
    report_lines.append('=' * 50)
    report_lines.append(f'Extraction Date: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}')
    report_lines.append(f'Source File: 001.xlsx')
    report_lines.append(f'Total Emails Extracted: {len(df)}')
    report_lines.append(f'Total Detection Signals: {len(df.columns)-1}')
    report_lines.append('')
    
    for idx, row in df.iterrows():
        data_id = row['Data ']
        signal_cols = df.columns[1:]
        active_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] != 0)
        report_lines.append(f'{data_id}: {active_count} active signals out of {len(signal_cols)}')
    
    # Save the report
    with open('/home/u3/email_data/check2/D76_D80_analysis_report.txt', 'w') as f:
        f.write('\n'.join(report_lines))
    
    print('Analysis complete. Report saved to D76_D80_analysis_report.txt')

if __name__ == '__main__':
    analyze_d76_d80()