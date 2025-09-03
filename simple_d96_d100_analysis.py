#!/usr/bin/env python3
"""
Simple and robust analysis for D96-D100 - Final batch analysis
"""

import pandas as pd
import numpy as np

def create_simple_analysis():
    # Read the extracted data
    df = pd.read_csv('/home/u3/email_data/check2/extracted_D96_D100_data.csv')
    
    # Clean column names (remove trailing spaces)
    df.columns = df.columns.str.strip()
    
    print("="*100)
    print("FINAL BATCH ANALYSIS: D96-D100 EMAIL CLASSIFICATION DATA")
    print("Completing the analysis of all 100 emails")
    print("="*100)
    print()
    
    print("EXTRACTED DATA:")
    print(f"- Number of emails: {len(df)}")
    print(f"- Number of detection signals: {len(df.columns) - 1}")
    print(f"- Email IDs: {', '.join(df.iloc[:, 0].astype(str).tolist())}")
    print()
    
    # Display the full data in a readable format
    print("COMPLETE DATA TABLE:")
    print("="*120)
    
    # Show first few columns
    print("\nFirst 10 columns:")
    print(df.iloc[:, :10].to_string(index=False))
    
    print("\nColumns 11-20:")
    if len(df.columns) > 10:
        end_col = min(20, len(df.columns))
        print(df.iloc[:, 10:end_col].to_string(index=False))
    
    print("\nColumns 21-30:")
    if len(df.columns) > 20:
        end_col = min(30, len(df.columns))
        print(df.iloc[:, 20:end_col].to_string(index=False))
    
    print("\nColumns 31-40:")
    if len(df.columns) > 30:
        end_col = min(40, len(df.columns))
        print(df.iloc[:, 30:end_col].to_string(index=False))
    
    print("\nColumns 41-50:")
    if len(df.columns) > 40:
        end_col = min(50, len(df.columns))
        print(df.iloc[:, 40:end_col].to_string(index=False))
    
    print("\nColumns 51-60:")
    if len(df.columns) > 50:
        end_col = min(60, len(df.columns))
        print(df.iloc[:, 50:end_col].to_string(index=False))
    
    print("\nRemaining columns:")
    if len(df.columns) > 60:
        print(df.iloc[:, 60:].to_string(index=False))
    
    print("\n" + "="*100)
    print("SIGNAL ANALYSIS FOR EACH EMAIL")
    print("="*100)
    
    # Analyze each email
    for idx, row in df.iterrows():
        email_id = str(row.iloc[0])
        print(f"\n{email_id} ANALYSIS:")
        print("-" * 40)
        
        # Find triggered signals (numeric values > 0)
        triggered_signals = []
        for col_idx, col_name in enumerate(df.columns[1:], 1):  # Skip first column (Data ID)
            value = row.iloc[col_idx]
            
            # Handle different types of values
            if pd.notna(value):
                try:
                    if isinstance(value, str):
                        if value.lower() not in ['pass', 'none', 'valid', 'softfail', 'fail', 'expired', 'neutral']:
                            # Skip non-numeric strings that aren't status values
                            continue
                        elif value.lower() in ['fail', 'expired', 'softfail']:
                            triggered_signals.append((col_name, value))
                    elif float(value) > 0:
                        triggered_signals.append((col_name, value))
                except (ValueError, TypeError):
                    continue
        
        print(f"Total signals triggered: {len(triggered_signals)}")
        
        if triggered_signals:
            print("Triggered signals:")
            for signal_name, signal_value in triggered_signals:
                if isinstance(signal_value, str):
                    print(f"  • {signal_name}: {signal_value}")
                else:
                    print(f"  • {signal_name}: {signal_value}")
        else:
            print("No significant signals triggered - appears to be a clean email")
        
        # Simple risk assessment
        signal_count = len(triggered_signals)
        if signal_count == 0:
            risk = "VERY LOW - Clean email"
        elif signal_count <= 2:
            risk = "LOW - Minor flags"
        elif signal_count <= 5:
            risk = "MEDIUM - Multiple flags"
        elif signal_count <= 10:
            risk = "HIGH - Many flags"
        else:
            risk = "VERY HIGH - Critical"
        
        print(f"Risk Assessment: {risk}")
    
    print("\n" + "="*100)
    print("BATCH SUMMARY")
    print("="*100)
    
    # Calculate summary statistics
    all_signal_counts = []
    for idx, row in df.iterrows():
        signal_count = 0
        for col_idx in range(1, len(df.columns)):
            value = row.iloc[col_idx]
            if pd.notna(value):
                try:
                    if isinstance(value, str):
                        if value.lower() in ['fail', 'expired', 'softfail']:
                            signal_count += 1
                    elif float(value) > 0:
                        signal_count += 1
                except (ValueError, TypeError):
                    continue
        all_signal_counts.append(signal_count)
    
    print(f"Signal statistics for D96-D100:")
    print(f"  • Average signals per email: {np.mean(all_signal_counts):.1f}")
    print(f"  • Range: {min(all_signal_counts)} - {max(all_signal_counts)} signals")
    print(f"  • Total unique signals analyzed: {len(df.columns) - 1}")
    
    # Risk distribution
    risk_levels = []
    for count in all_signal_counts:
        if count == 0:
            risk_levels.append("VERY LOW")
        elif count <= 2:
            risk_levels.append("LOW")
        elif count <= 5:
            risk_levels.append("MEDIUM")
        elif count <= 10:
            risk_levels.append("HIGH")
        else:
            risk_levels.append("VERY HIGH")
    
    from collections import Counter
    risk_dist = Counter(risk_levels)
    print(f"\nRisk distribution:")
    for risk, count in risk_dist.items():
        print(f"  • {risk}: {count} emails")
    
    print(f"\n✓ ANALYSIS COMPLETE")
    print(f"✓ Final batch D96-D100 processed successfully")
    print(f"✓ All 100 emails (D1-D100) analysis now complete")
    
    # Save summary to file
    summary_lines = [
        "D96-D100 FINAL BATCH SUMMARY",
        "=" * 50,
        "",
        f"Emails analyzed: {', '.join(df.iloc[:, 0].astype(str).tolist())}",
        f"Detection signals per email: {all_signal_counts}",
        f"Average signals: {np.mean(all_signal_counts):.1f}",
        f"Risk levels: {risk_levels}",
        "",
        "Individual email details:",
    ]
    
    for idx, (email_id, signal_count, risk) in enumerate(zip(df.iloc[:, 0].astype(str), all_signal_counts, risk_levels)):
        summary_lines.append(f"  {email_id}: {signal_count} signals, {risk} risk")
    
    summary_lines.extend([
        "",
        "COMPLETION STATUS:",
        "✓ All 100 emails analyzed",
        "✓ Ready for final decision making"
    ])
    
    summary_path = '/home/u3/email_data/check2/D96_D100_final_summary.txt'
    with open(summary_path, 'w') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"\nSummary saved to: {summary_path}")

if __name__ == "__main__":
    create_simple_analysis()