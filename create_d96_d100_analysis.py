#!/usr/bin/env python3
"""
Create detailed analysis report for D96-D100 - Final batch analysis
"""

import pandas as pd
import numpy as np

def create_detailed_analysis():
    # Read the extracted data
    df = pd.read_csv('/home/u3/email_data/check2/extracted_D96_D100_data.csv')
    
    # Get column information
    print("Available columns:", df.columns.tolist())
    data_id_col = df.columns[0]  # First column should be the data ID
    signal_cols = [col for col in df.columns if col != data_id_col]
    
    # Create comprehensive analysis report
    report_lines = []
    report_lines.append("="*100)
    report_lines.append("FINAL BATCH ANALYSIS: D96-D100 EMAIL CLASSIFICATION DATA")
    report_lines.append("Completing the analysis of all 100 emails")
    report_lines.append("="*100)
    report_lines.append("")
    
    # Overall summary
    report_lines.append("BATCH OVERVIEW:")
    report_lines.append(f"- Email IDs: D96, D97, D98, D99, D100")
    report_lines.append(f"- Total detection signals analyzed: {len(signal_cols)}")
    report_lines.append(f"- Data source: 001.xlsx")
    report_lines.append("")
    
    # Detailed analysis for each email
    for idx, row in df.iterrows():
        email_id = row[data_id_col]
        report_lines.append(f"{'='*60}")
        report_lines.append(f"EMAIL {email_id} DETAILED ANALYSIS")
        report_lines.append(f"{'='*60}")
        
        # Categorize signals
        sender_signals = []
        attachment_signals = []
        content_signals = []
        auth_signals = []
        url_signals = []
        behavioral_signals = []
        other_signals = []
        
        triggered_signals = []
        
        for col in signal_cols:
            value = row[col]
            if pd.notna(value) and value > 0:
                triggered_signals.append((col, value))
                
                # Categorize the signal
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['sender', 'domain_reputation', 'spf', 'dkim', 'dmarc', 'return_path', 'reply_path']):
                    if 'sender' in col_lower or 'domain' in col_lower or 'return_path' in col_lower or 'reply_path' in col_lower:
                        sender_signals.append((col, value))
                    else:
                        auth_signals.append((col, value))
                elif any(keyword in col_lower for keyword in ['attachment', 'file', 'hash', 'metadata', 'executable', 'macro', 'vbscript', 'javascript']):
                    attachment_signals.append((col, value))
                elif any(keyword in col_lower for keyword in ['content', 'spam', 'urgency', 'html', 'image', 'marketing']):
                    content_signals.append((col, value))
                elif any(keyword in col_lower for keyword in ['url', 'link', 'redirect', 'ssl', 'site']):
                    url_signals.append((col, value))
                elif any(keyword in col_lower for keyword in ['behavior', 'sandbox', 'execution', 'process']):
                    behavioral_signals.append((col, value))
                else:
                    other_signals.append((col, value))
        
        # Summary for this email
        report_lines.append(f"Total signals triggered: {len(triggered_signals)}")
        report_lines.append(f"Signal distribution:")
        report_lines.append(f"  - Sender/Domain signals: {len(sender_signals)}")
        report_lines.append(f"  - Authentication signals: {len(auth_signals)}")
        report_lines.append(f"  - Attachment signals: {len(attachment_signals)}")
        report_lines.append(f"  - Content signals: {len(content_signals)}")
        report_lines.append(f"  - URL/Link signals: {len(url_signals)}")
        report_lines.append(f"  - Behavioral signals: {len(behavioral_signals)}")
        report_lines.append(f"  - Other signals: {len(other_signals)}")
        report_lines.append("")
        
        # List all triggered signals
        if triggered_signals:
            report_lines.append("TRIGGERED SIGNALS:")
            for signal_name, signal_value in triggered_signals:
                if signal_value == 1:
                    report_lines.append(f"  ✓ {signal_name}: DETECTED")
                else:
                    report_lines.append(f"  ⚠ {signal_name}: {signal_value}")
        else:
            report_lines.append("No signals triggered - Clean email")
        
        report_lines.append("")
        
        # Risk assessment
        total_triggered = len(triggered_signals)
        if total_triggered == 0:
            risk_level = "VERY LOW"
        elif total_triggered <= 2:
            risk_level = "LOW"
        elif total_triggered <= 5:
            risk_level = "MEDIUM"
        elif total_triggered <= 10:
            risk_level = "HIGH"
        else:
            risk_level = "VERY HIGH"
        
        report_lines.append(f"RISK ASSESSMENT: {risk_level}")
        report_lines.append(f"Recommendation: {'Investigate further' if total_triggered > 5 else 'Monitor' if total_triggered > 2 else 'Likely legitimate'}")
        report_lines.append("")
    
    # Final batch summary
    report_lines.append("="*100)
    report_lines.append("FINAL BATCH SUMMARY (D96-D100)")
    report_lines.append("="*100)
    
    # Calculate batch statistics
    email_risk_levels = []
    total_signals_per_email = []
    
    for idx, row in df.iterrows():
        email_id = row[data_id_col]
        triggered_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] > 0)
        total_signals_per_email.append(triggered_count)
        
        if triggered_count == 0:
            risk = "VERY LOW"
        elif triggered_count <= 2:
            risk = "LOW"
        elif triggered_count <= 5:
            risk = "MEDIUM"
        elif triggered_count <= 10:
            risk = "HIGH"
        else:
            risk = "VERY HIGH"
        
        email_risk_levels.append(risk)
        report_lines.append(f"{email_id}: {triggered_count} signals triggered - {risk} risk")
    
    report_lines.append("")
    report_lines.append("BATCH STATISTICS:")
    report_lines.append(f"- Average signals per email: {np.mean(total_signals_per_email):.1f}")
    report_lines.append(f"- Range of signals: {min(total_signals_per_email)} - {max(total_signals_per_email)}")
    report_lines.append(f"- Risk distribution:")
    
    from collections import Counter
    risk_counts = Counter(email_risk_levels)
    for risk, count in risk_counts.items():
        report_lines.append(f"  - {risk}: {count} emails")
    
    report_lines.append("")
    report_lines.append("ANALYSIS COMPLETION STATUS:")
    report_lines.append("✓ All 100 emails (D1-D100) have been analyzed")
    report_lines.append("✓ Final batch D96-D100 processing complete")
    report_lines.append("✓ Ready for final decision making and action planning")
    
    # Save the report
    report_path = '/home/u3/email_data/check2/D96_D100_final_analysis.txt'
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    print('\n'.join(report_lines))
    print(f"\nDetailed analysis report saved to: {report_path}")
    
    # Also create a summary CSV for easy analysis
    summary_data = []
    for idx, row in df.iterrows():
        email_id = row[data_id_col]
        triggered_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] > 0)
        
        if triggered_count == 0:
            risk = "VERY LOW"
        elif triggered_count <= 2:
            risk = "LOW"
        elif triggered_count <= 5:
            risk = "MEDIUM"
        elif triggered_count <= 10:
            risk = "HIGH"
        else:
            risk = "VERY HIGH"
        
        # Get specific signal categories
        sender_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] > 0 and 
                          any(keyword in col.lower() for keyword in ['sender', 'domain_reputation', 'return_path', 'reply_path']))
        auth_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] > 0 and 
                        any(keyword in col.lower() for keyword in ['spf', 'dkim', 'dmarc']))
        attachment_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] > 0 and 
                              any(keyword in col.lower() for keyword in ['attachment', 'file', 'hash', 'metadata', 'executable', 'macro']))
        content_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] > 0 and 
                           any(keyword in col.lower() for keyword in ['content', 'spam', 'urgency', 'html', 'marketing']))
        url_count = sum(1 for col in signal_cols if pd.notna(row[col]) and row[col] > 0 and 
                       any(keyword in col.lower() for keyword in ['url', 'link', 'redirect', 'ssl', 'site']))
        
        summary_data.append({
            'Email_ID': email_id,
            'Total_Signals_Triggered': triggered_count,
            'Risk_Level': risk,
            'Sender_Signals': sender_count,
            'Auth_Signals': auth_count,
            'Attachment_Signals': attachment_count,
            'Content_Signals': content_count,
            'URL_Signals': url_count
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_csv_path = '/home/u3/email_data/check2/D96_D100_summary_analysis.csv'
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"Summary analysis CSV saved to: {summary_csv_path}")

if __name__ == "__main__":
    create_detailed_analysis()