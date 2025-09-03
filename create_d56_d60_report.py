import pandas as pd

# Read the extracted data
df = pd.read_csv('extracted_D56_D60_data.csv')

# Create a readable text report
with open('D56_D60_analysis_report.txt', 'w') as f:
    f.write('EMAIL CLASSIFICATION DATA ANALYSIS\n')
    f.write('=================================\n')
    f.write('Data extracted for: D56, D57, D58, D59, D60\n')
    f.write(f'Total detection signals: {len(df.columns) - 1}\n\n')
    
    # For each email ID
    for idx, row in df.iterrows():
        email_id = row['Data ']
        f.write(f'\n{"="*60}\n')
        f.write(f'EMAIL ID: {email_id}\n')
        f.write(f'{"="*60}\n\n')
        
        # Group signals for better readability
        signal_groups = {
            'Sender Signals': ['sender_known_malicios', 'sender_domain_reputation_score', 
                              'sender_spoof_detected', 'sender_temp_email_likelihood'],
            'Authentication': ['dmarc_enforced', 'SPF_Pass', 'dkim_check_passed'],
            'Attachment Analysis': ['packer_detected', 'any_file_hash_malicious', 
                                   'max_metadata_suspicious_score', 'malicious_attachment_Count',
                                   'unusual_file_extensions_count'],
            'URL/Link Analysis': ['url_reputation_score', 'hyperlink_mismatch_count',
                                 'url_shortener_count', 'link_rewritten_through_redirector',
                                 'homoglyph_detected_in_URL']
        }
        
        # Print grouped signals
        for group_name, signal_list in signal_groups.items():
            f.write(f'{group_name}:\n')
            for signal in signal_list:
                if signal in df.columns:
                    value = row[signal]
                    f.write(f'  - {signal}: {value}\n')
            f.write('\n')
        
        # Print remaining signals
        f.write('Other Detection Signals:\n')
        printed_signals = set()
        for group_signals in signal_groups.values():
            printed_signals.update(group_signals)
        
        for col in df.columns:
            if col != 'Data ' and col not in printed_signals:
                value = row[col]
                f.write(f'  - {col}: {value}\n')
        
        f.write('\n')

print('Readable report created: D56_D60_analysis_report.txt')

# Also create a summary showing non-zero/non-null values for each email
print('\n=== SUMMARY OF NON-ZERO VALUES ===\n')
for idx, row in df.iterrows():
    email_id = row['Data ']
    non_zero_signals = []
    for col in df.columns:
        if col != 'Data ':
            value = row[col]
            if pd.notna(value) and value != 0 and value != '0':
                non_zero_signals.append(f'{col}={value}')
    
    print(f'{email_id}: {len(non_zero_signals)} active signals')
    if len(non_zero_signals) <= 10:
        for signal in non_zero_signals:
            print(f'  - {signal}')
    else:
        print(f'  - First 5: {", ".join(non_zero_signals[:5])}')
        print(f'  - ...')
        print(f'  - Last 5: {", ".join(non_zero_signals[-5:])}')
    print()