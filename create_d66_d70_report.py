import pandas as pd

# Read the extracted data
df = pd.read_csv('/home/u3/email_data/check2/extracted_D66_D70_data.csv')

print('=' * 80)
print('EMAIL CLASSIFICATION DATA ANALYSIS - D66 TO D70')
print('=' * 80)
print()

for index, row in df.iterrows():
    data_id = row['Data ']
    print(f'EMAIL {data_id}:')
    print('-' * 40)
    
    # Count non-zero detection signals
    signal_columns = [col for col in df.columns if col != 'Data ']
    non_zero_signals = sum(1 for col in signal_columns if row[col] != 0)
    total_signals = len(signal_columns)
    
    print(f'Total Detection Signals: {total_signals}')
    print(f'Active Signals (non-zero): {non_zero_signals}')
    print(f'Inactive Signals (zero): {total_signals - non_zero_signals}')
    
    # Show active signals with their values
    print('\nActive Detection Signals:')
    active_signals = []
    for col in signal_columns:
        if row[col] != 0:
            active_signals.append(f'  {col}: {row[col]}')
    
    if active_signals:
        for signal in sorted(active_signals):
            print(signal)
    else:
        print('  No active signals detected')
    
    print()
    print('=' * 80)
    print()

print('\nSUMMARY:')
print(f'Total emails analyzed: {len(df)}')
print(f'Data range: D66 to D70')
print(f'Detection signals per email: {len(signal_columns)}')

# Also create a simplified CSV with just the active signals
print('\nCreating simplified analysis...')
simplified_data = []

for index, row in df.iterrows():
    data_id = row['Data ']
    signal_columns = [col for col in df.columns if col != 'Data ']
    active_signals = {col: row[col] for col in signal_columns if row[col] != 0}
    
    simplified_data.append({
        'Data_ID': data_id,
        'Total_Signals': len(signal_columns),
        'Active_Signals': len(active_signals),
        'Active_Signal_Details': str(active_signals) if active_signals else 'None'
    })

simplified_df = pd.DataFrame(simplified_data)
simplified_df.to_csv('/home/u3/email_data/check2/D66_D70_simplified_analysis.csv', index=False)

print('Files created:')
print('- extracted_D66_D70_data.csv (full data)')
print('- extracted_D66_D70_data.xlsx (full data)')
print('- D66_D70_simplified_analysis.csv (summary)')