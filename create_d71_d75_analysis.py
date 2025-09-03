import pandas as pd
import numpy as np

# Read the extracted data
df = pd.read_csv('extracted_D71_D75_data.csv')

print("=== EMAIL CLASSIFICATION DATA: D71-D75 ANALYSIS ===")
print(f"Total emails analyzed: {len(df)}")
print(f"Total detection signals: {len(df.columns)-1}")  # Subtract 1 for Data ID column
print()

# Create a readable analysis for each email
for idx, row in df.iterrows():
    email_id = row['Data ']  # Note the space in column name
    print(f"=== EMAIL {email_id} ===")
    
    # Categorize signals by type
    sender_signals = []
    attachment_signals = []
    content_signals = []
    url_signals = []
    auth_signals = []
    other_signals = []
    
    # Categorize and display significant signals (non-zero values)
    for col in df.columns[1:]:  # Skip the Data ID column
        value = row[col]
        if pd.notna(value) and value != 0:
            signal_info = f"  {col}: {value}"
            
            # Categorize by signal type
            col_lower = col.lower()
            if 'sender' in col_lower or 'from' in col_lower or 'reply' in col_lower:
                sender_signals.append(signal_info)
            elif 'attachment' in col_lower or 'file' in col_lower or 'executable' in col_lower or 'macro' in col_lower:
                attachment_signals.append(signal_info)
            elif 'content' in col_lower or 'spam' in col_lower or 'keyword' in col_lower or 'html' in col_lower:
                content_signals.append(signal_info)
            elif 'url' in col_lower or 'link' in col_lower or 'domain' in col_lower:
                url_signals.append(signal_info)
            elif 'spf' in col_lower or 'dkim' in col_lower or 'dmarc' in col_lower or 'dns' in col_lower or 'tls' in col_lower:
                auth_signals.append(signal_info)
            else:
                other_signals.append(signal_info)
    
    # Display categorized signals
    if sender_signals:
        print("SENDER SIGNALS:")
        for signal in sender_signals:
            print(signal)
        print()
    
    if attachment_signals:
        print("ATTACHMENT SIGNALS:")
        for signal in attachment_signals:
            print(signal)
        print()
    
    if content_signals:
        print("CONTENT SIGNALS:")
        for signal in content_signals:
            print(signal)
        print()
    
    if url_signals:
        print("URL/DOMAIN SIGNALS:")
        for signal in url_signals:
            print(signal)
        print()
    
    if auth_signals:
        print("AUTHENTICATION SIGNALS:")
        for signal in auth_signals:
            print(signal)
        print()
    
    if other_signals:
        print("OTHER SIGNALS:")
        for signal in other_signals:
            print(signal)
        print()
    
    # Count total active signals
    total_active_signals = sum(1 for col in df.columns[1:] if pd.notna(row[col]) and row[col] != 0)
    print(f"Total active detection signals: {total_active_signals}")
    print("-" * 50)
    print()

# Create a summary comparison table
print("=== SUMMARY COMPARISON TABLE ===")
print("\nKey Detection Signals Summary:")
print("-" * 80)

# Select some key indicators for comparison
key_columns = [
    'Data ', 'sender_known_malicios', 'sender_domain_reputation_score', 
    'malicious_attachment_Count', 'total_yara_match_count', 'total_ioc_count',
    'content_spam_score', 'url_Count', 'final_url_known_malicious',
    'spf_result', 'dkim_result', 'dmarc_result'
]

# Filter to only columns that exist
existing_key_columns = [col for col in key_columns if col in df.columns]

summary_df = df[existing_key_columns]
print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("Analysis complete. Full data available in:")
print("- extracted_D71_D75_data.csv")
print("- extracted_D71_D75_data.xlsx")