import pandas as pd

# Read the extracted data
df = pd.read_csv('/home/u3/email_data/check2/extracted_D81_D85_data.csv')

print('=== DETAILED ANALYSIS OF D81-D85 EMAIL DATA ===\n')

# Display basic info
print(f'Total records: {len(df)}')
print(f'Total detection signals: {len(df.columns) - 1}')  # Minus 1 for Data ID column
print(f'Data IDs: {df["Data "].tolist()}\n')

# Analyze each email
for idx, row in df.iterrows():
    data_id = row['Data ']
    print(f'--- {data_id} ---')
    
    # Find non-zero/non-null signals
    active_signals = {}
    for col in df.columns[1:]:  # Skip Data ID column
        value = row[col]
        if pd.notna(value) and value != 0 and value != '':
            active_signals[col] = value
    
    print(f'Active signals: {len(active_signals)} out of {len(df.columns) - 1}')
    
    if active_signals:
        print('Signal details:')
        for signal, value in sorted(active_signals.items()):
            print(f'  {signal}: {value}')
    else:
        print('No active signals (all values are 0 or null)')
    print()

# Create a summary report
print('\n=== SUMMARY REPORT ===')
with open('/home/u3/email_data/check2/D81_D85_analysis_report.txt', 'w') as f:
    f.write('EMAIL CLASSIFICATION DATA ANALYSIS - D81 to D85\n')
    f.write('=' * 50 + '\n\n')
    
    f.write(f'Analysis Date: 2025-09-03\n')
    f.write(f'Source File: 001.xlsx\n')
    f.write(f'Records Analyzed: {len(df)}\n')
    f.write(f'Detection Signals: {len(df.columns) - 1}\n\n')
    
    for idx, row in df.iterrows():
        data_id = row['Data ']
        f.write(f'{data_id}:\n')
        
        # Find active signals
        active_signals = {}
        for col in df.columns[1:]:
            value = row[col]
            if pd.notna(value) and value != 0 and value != '':
                active_signals[col] = value
        
        f.write(f'  Active Signals: {len(active_signals)}/{len(df.columns) - 1}\n')
        
        if active_signals:
            f.write('  Signal Details:\n')
            for signal, value in sorted(active_signals.items()):
                f.write(f'    {signal}: {value}\n')
        else:
            f.write('  No active signals detected\n')
        f.write('\n')

print('Analysis complete! Files created:')
print('- /home/u3/email_data/check2/extracted_D81_D85_data.csv')
print('- /home/u3/email_data/check2/extracted_D81_D85_data.xlsx') 
print('- /home/u3/email_data/check2/D81_D85_analysis_report.txt')