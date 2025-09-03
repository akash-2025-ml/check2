import pandas as pd
import numpy as np

# Read the extracted data
df = pd.read_csv('/home/u3/email_data/check2/extracted_D91_D95_data.csv')

print('='*80)
print('EXTRACTED EMAIL DATA: D91, D92, D93, D94, D95')
print('='*80)
print(f'Dataset contains {len(df)} emails with {len(df.columns)-1} detection signals')
print()

def safe_numeric_conversion(value):
    """Safely convert value to numeric, return 0 if not possible"""
    try:
        if pd.isna(value) or value == '':
            return 0
        if isinstance(value, str):
            # Handle string representations of numbers
            if value.strip() == '':
                return 0
            # Try to convert to float
            return float(value)
        return float(value)
    except (ValueError, TypeError):
        return 0

# Display basic info for each email
for idx, row in df.iterrows():
    email_id = row['Data ']
    print(f'Email ID: {email_id}')
    
    # Count non-zero signals
    signal_columns = df.columns[1:]  # All columns except 'Data '
    
    # Count active signals and calculate total score
    active_signals = 0
    numeric_total = 0
    
    for col in signal_columns:
        value = safe_numeric_conversion(row[col])
        if value != 0:
            active_signals += 1
            numeric_total += value
    
    print(f'  - Active signals (non-zero): {active_signals} out of {len(signal_columns)}')
    print(f'  - Total numeric signal score: {numeric_total:.6f}')
    
    # Show top 5 highest scoring signals (numeric values only)
    signal_scores = []
    for col in signal_columns:
        value = safe_numeric_conversion(row[col])
        if value > 0:
            signal_scores.append((col, value))
    
    signal_scores.sort(key=lambda x: x[1], reverse=True)
    
    if signal_scores:
        print(f'  - Top numeric signals:')
        for signal, score in signal_scores[:5]:
            print(f'    * {signal}: {score:.6f}')
    else:
        print('  - No active numeric signals detected')
    
    print()

# Create a detailed analysis report
print('='*80)
print('DETAILED SIGNAL ANALYSIS')
print('='*80)

# Show all signal values for each email
print('\nDetailed Signal Values (showing all non-zero values):')
print('-' * 80)

for idx, row in df.iterrows():
    email_id = row['Data ']
    print(f'\n{email_id}:')
    
    signal_columns = df.columns[1:]
    active_signals = []
    
    for col in signal_columns:
        value = row[col]
        numeric_value = safe_numeric_conversion(value)
        
        if numeric_value != 0 or (isinstance(value, str) and value.strip() != '' and value != '0'):
            if isinstance(value, str) and not value.replace('.', '').replace('-', '').replace('e', '').isdigit():
                active_signals.append(f'{col}: "{value}" (text)')
            else:
                active_signals.append(f'{col}: {numeric_value:.6f}')
    
    if active_signals:
        for signal in active_signals[:15]:  # Show top 15 to keep it readable
            print(f'  {signal}')
        if len(active_signals) > 15:
            print(f'  ... and {len(active_signals) - 15} more signals')
    else:
        print('  No active signals')

# Summary statistics
print('\n' + '='*80)
print('SUMMARY STATISTICS')
print('='*80)

signal_columns = df.columns[1:]
print(f'Total detection signals available: {len(signal_columns)}')

for idx, row in df.iterrows():
    email_id = row['Data ']
    active_count = sum(1 for col in signal_columns if safe_numeric_conversion(row[col]) != 0)
    total_score = sum(safe_numeric_conversion(row[col]) for col in signal_columns)
    
    print(f'{email_id}: {active_count} active signals, total score: {total_score:.6f}')