#!/usr/bin/env python3
"""
Create a detailed readable analysis report for D86-D90 extracted data
"""

import pandas as pd
import numpy as np

def create_readable_report():
    try:
        # Read the extracted data
        df = pd.read_csv('extracted_D86_D90_data.csv')
        
        # Create detailed analysis report
        report_filename = 'D86_D90_analysis_report.txt'
        
        with open(report_filename, 'w') as f:
            f.write("="*100 + "\n")
            f.write("DETAILED ANALYSIS REPORT: EMAIL DATA D86-D90\n")
            f.write("="*100 + "\n\n")
            
            f.write(f"Total emails analyzed: {len(df)}\n")
            f.write(f"Total detection signals: {len(df.columns) - 1}\n")
            f.write(f"Data extracted from: 001.xlsx\n\n")
            
            # Analyze each email in detail
            data_id_col = df.columns[0]
            
            for idx, row in df.iterrows():
                data_id = row[data_id_col]
                f.write("="*80 + "\n")
                f.write(f"EMAIL: {data_id}\n")
                f.write("="*80 + "\n\n")
                
                # Categorize signals by type
                sender_signals = {}
                attachment_signals = {}
                domain_signals = {}
                behavioral_signals = {}
                reputation_signals = {}
                other_signals = {}
                
                for col in df.columns[1:]:
                    value = row[col]
                    if pd.notna(value) and value != 0:
                        if 'sender' in col.lower():
                            sender_signals[col] = value
                        elif 'attachment' in col.lower() or 'file' in col.lower() or 'executable' in col.lower() or 'macro' in col.lower():
                            attachment_signals[col] = value
                        elif 'domain' in col.lower() or 'url' in col.lower():
                            domain_signals[col] = value
                        elif 'behavioral' in col.lower() or 'sandbox' in col.lower() or 'behavior' in col.lower() or 'execution' in col.lower():
                            behavioral_signals[col] = value
                        elif 'reputation' in col.lower() or 'ip' in col.lower() or 'smtp' in col.lower():
                            reputation_signals[col] = value
                        else:
                            other_signals[col] = value
                
                # Write categorized signals
                if sender_signals:
                    f.write("SENDER-RELATED SIGNALS:\n")
                    f.write("-" * 30 + "\n")
                    for signal, value in sender_signals.items():
                        f.write(f"  {signal}: {value}\n")
                    f.write("\n")
                
                if attachment_signals:
                    f.write("ATTACHMENT-RELATED SIGNALS:\n")
                    f.write("-" * 30 + "\n")
                    for signal, value in attachment_signals.items():
                        f.write(f"  {signal}: {value}\n")
                    f.write("\n")
                
                if domain_signals:
                    f.write("DOMAIN/URL-RELATED SIGNALS:\n")
                    f.write("-" * 30 + "\n")
                    for signal, value in domain_signals.items():
                        f.write(f"  {signal}: {value}\n")
                    f.write("\n")
                
                if behavioral_signals:
                    f.write("BEHAVIORAL ANALYSIS SIGNALS:\n")
                    f.write("-" * 30 + "\n")
                    for signal, value in behavioral_signals.items():
                        f.write(f"  {signal}: {value}\n")
                    f.write("\n")
                
                if reputation_signals:
                    f.write("REPUTATION/NETWORK SIGNALS:\n")
                    f.write("-" * 30 + "\n")
                    for signal, value in reputation_signals.items():
                        f.write(f"  {signal}: {value}\n")
                    f.write("\n")
                
                if other_signals:
                    f.write("OTHER SIGNALS:\n")
                    f.write("-" * 30 + "\n")
                    for signal, value in other_signals.items():
                        f.write(f"  {signal}: {value}\n")
                    f.write("\n")
                
                # Risk assessment
                total_signals = len(sender_signals) + len(attachment_signals) + len(domain_signals) + len(behavioral_signals) + len(reputation_signals) + len(other_signals)
                f.write(f"RISK SUMMARY:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total active signals: {total_signals}/68\n")
                f.write(f"Signal activity percentage: {total_signals/68*100:.1f}%\n")
                
                # Highlight high-risk indicators
                high_risk_indicators = []
                for col in df.columns[1:]:
                    value = row[col]
                    if pd.notna(value) and value != 0:
                        # Check for high-risk signals based on signal name and value
                        if ('malicious' in col.lower() and value > 0) or \
                           ('suspicious' in col.lower() and value > 0.5) or \
                           ('behavioral_sandbox_score' in col.lower() and value > 0.2) or \
                           ('exfiltration' in col.lower() and value > 0.5) or \
                           ('temp_email' in col.lower() and value > 0.5):
                            high_risk_indicators.append((col, value))
                
                if high_risk_indicators:
                    f.write(f"\nHIGH RISK INDICATORS:\n")
                    f.write("-" * 30 + "\n")
                    for signal, value in high_risk_indicators:
                        f.write(f"  ⚠️  {signal}: {value}\n")
                else:
                    f.write(f"\nNo high-risk indicators detected.\n")
                
                f.write("\n")
            
            # Comparative analysis
            f.write("="*100 + "\n")
            f.write("COMPARATIVE ANALYSIS\n")
            f.write("="*100 + "\n\n")
            
            # Signal activity comparison
            f.write("SIGNAL ACTIVITY COMPARISON:\n")
            f.write("-" * 40 + "\n")
            for idx, row in df.iterrows():
                data_id = row[data_id_col]
                active_signals = sum(1 for val in row[1:] if pd.notna(val) and val != 0)
                f.write(f"{data_id}: {active_signals}/68 signals ({active_signals/68*100:.1f}%)\n")
            
            f.write("\n")
            
            # Most common active signals across all emails
            f.write("MOST COMMON ACTIVE SIGNALS:\n")
            f.write("-" * 40 + "\n")
            
            signal_counts = {}
            for col in df.columns[1:]:
                count = sum(1 for val in df[col] if pd.notna(val) and val != 0)
                if count > 0:
                    signal_counts[col] = count
            
            # Sort by frequency
            sorted_signals = sorted(signal_counts.items(), key=lambda x: x[1], reverse=True)
            
            for signal, count in sorted_signals[:20]:  # Top 20
                f.write(f"{signal}: active in {count}/5 emails ({count/5*100:.0f}%)\n")
            
            f.write("\n")
            
            # Summary conclusions
            f.write("SUMMARY CONCLUSIONS:\n")
            f.write("-" * 40 + "\n")
            
            # Find email with most activity
            max_activity_idx = 0
            max_activity_count = 0
            for idx, row in df.iterrows():
                active_signals = sum(1 for val in row[1:] if pd.notna(val) and val != 0)
                if active_signals > max_activity_count:
                    max_activity_count = active_signals
                    max_activity_idx = idx
            
            most_active_email = df.iloc[max_activity_idx][data_id_col]
            f.write(f"Most active email: {most_active_email} with {max_activity_count} signals\n")
            
            # Find email with least activity
            min_activity_idx = 0
            min_activity_count = 68
            for idx, row in df.iterrows():
                active_signals = sum(1 for val in row[1:] if pd.notna(val) and val != 0)
                if active_signals < min_activity_count:
                    min_activity_count = active_signals
                    min_activity_idx = idx
            
            least_active_email = df.iloc[min_activity_idx][data_id_col]
            f.write(f"Least active email: {least_active_email} with {min_activity_count} signals\n")
            
            avg_activity = sum(sum(1 for val in row[1:] if pd.notna(val) and val != 0) for _, row in df.iterrows()) / len(df)
            f.write(f"Average signal activity: {avg_activity:.1f} signals per email\n")
            
        print(f"Detailed analysis report created: {report_filename}")
        
        # Also create a simplified CSV with just the key information
        simple_report_filename = 'D86_D90_simplified_analysis.csv'
        
        # Create summary data
        summary_data = []
        for idx, row in df.iterrows():
            data_id = row[data_id_col]
            active_signals = sum(1 for val in row[1:] if pd.notna(val) and val != 0)
            
            # Count high-risk signals
            high_risk_count = 0
            high_risk_details = []
            
            for col in df.columns[1:]:
                value = row[col]
                if pd.notna(value) and value != 0:
                    if ('malicious' in col.lower() and value > 0) or \
                       ('suspicious' in col.lower() and value > 0.5) or \
                       ('behavioral_sandbox_score' in col.lower() and value > 0.2) or \
                       ('exfiltration' in col.lower() and value > 0.5) or \
                       ('temp_email' in col.lower() and value > 0.5):
                        high_risk_count += 1
                        high_risk_details.append(f"{col}:{value}")
            
            summary_data.append({
                'Email_ID': data_id,
                'Total_Active_Signals': active_signals,
                'Signal_Activity_Percentage': f"{active_signals/68*100:.1f}%",
                'High_Risk_Signals': high_risk_count,
                'High_Risk_Details': '; '.join(high_risk_details[:3]) if high_risk_details else 'None'
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(simple_report_filename, index=False)
        print(f"Simplified analysis created: {simple_report_filename}")
        
        return True
        
    except Exception as e:
        print(f"Error creating report: {e}")
        return False

if __name__ == "__main__":
    create_readable_report()