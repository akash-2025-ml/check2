import pandas as pd
import numpy as np

def create_readable_report():
    """Create a readable analysis report for the D51-D55 email data"""
    
    # Read the extracted data
    df = pd.read_csv('extracted_D51_D55_data.csv')
    
    print("="*80)
    print("EMAIL CLASSIFICATION DATA ANALYSIS - D51 TO D55")
    print("="*80)
    print()
    
    print(f"Dataset Summary:")
    print(f"- Number of emails analyzed: {len(df)}")
    print(f"- Total detection signals: {len(df.columns) - 1}")  # Minus the ID column
    print(f"- Email IDs: {', '.join(df['Data '].astype(str).tolist())}")
    print()
    
    # Create a summary of key risk indicators
    print("KEY RISK INDICATORS SUMMARY:")
    print("-" * 50)
    
    # Define key security indicators to highlight
    key_indicators = [
        'sender_known_malicios',
        'sender_spoof_detected', 
        'packer_detected',
        'any_file_hash_malicious',
        'malicious_attachment_Count',
        'has_executable_attachment',
        'total_yara_match_count',
        'total_ioc_count',
        'any_macro_enabled_document',
        'any_exploit_pattern_detected',
        'return_path_known_malicious',
        'smtp_ip_known_malicious',
        'domain_known_malicious',
        'final_url_known_malicious',
        'total_components_detected_malicious'
    ]
    
    for email_id in df['Data '].astype(str):
        email_row = df[df['Data '] == email_id].iloc[0]
        print(f"\n{email_id}:")
        
        # Check for any high-risk indicators
        high_risk_found = False
        for indicator in key_indicators:
            if indicator in df.columns:
                value = email_row[indicator]
                if pd.notna(value) and value > 0:
                    print(f"  ⚠️  {indicator}: {value}")
                    high_risk_found = True
        
        if not high_risk_found:
            print("  ✅ No major malicious indicators detected")
            
        # Show some key scores
        score_indicators = [
            'sender_domain_reputation_score',
            'max_behavioral_sandbox_score',
            'content_spam_score',
            'url_reputation_score'
        ]
        
        scores_found = False
        for score in score_indicators:
            if score in df.columns:
                value = email_row[score]
                if pd.notna(value) and value > 0:
                    if not scores_found:
                        print("  📊 Key Scores:")
                        scores_found = True
                    print(f"     {score}: {value:.4f}")
    
    print("\n" + "="*80)
    print("DETAILED DATA TABLE")
    print("="*80)
    
    # Create a transposed view for better readability
    df_transposed = df.set_index('Data ').T
    
    # Save detailed report to file
    with open('D51_D55_analysis_report.txt', 'w') as f:
        f.write("EMAIL CLASSIFICATION DATA - DETAILED ANALYSIS\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Email IDs Analyzed: {', '.join(df['Data '].astype(str).tolist())}\n")
        f.write(f"Total Detection Signals: {len(df.columns) - 1}\n\n")
        
        f.write("SIGNAL VALUES BY EMAIL ID:\n")
        f.write("-" * 50 + "\n\n")
        
        # Write each signal and its values across all emails
        for column in df.columns[1:]:  # Skip the ID column
            f.write(f"{column}:\n")
            for email_id in df['Data '].astype(str):
                email_row = df[df['Data '] == email_id].iloc[0]
                value = email_row[column]
                f.write(f"  {email_id}: {value}\n")
            f.write("\n")
    
    print(f"\nDetailed analysis saved to: D51_D55_analysis_report.txt")
    print(f"Original data files created:")
    print(f"- extracted_D51_D55_data.csv (CSV format)")
    print(f"- extracted_D51_D55_data.xlsx (Excel format)")
    
    return df

if __name__ == "__main__":
    result = create_readable_report()