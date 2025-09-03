#!/usr/bin/env python3
import csv

# Read the CSV file
with open('001.csv', 'r') as f:
    reader = csv.DictReader(f)
    records = list(reader)

# Find records currently classified as No Action (1)
print("Records currently classified as No Action (value = 1):")
print("=" * 80)

no_action_records = []
for record in records:
    record_id = record['Data ']
    classification = int(record['total_components_detected_malicious'])
    
    if classification == 1:
        no_action_records.append(record)
        print(f"\n{record_id}:")
        print(f"  Sender reputation: {float(record['sender_domain_reputation_score']):.4f}")
        print(f"  Spam score: {float(record['content_spam_score']):.10f}")
        print(f"  Temp email likelihood: {float(record['sender_temp_email_likelihood']):.4f}")
        print(f"  Request type: {record['request_type']}")
        print(f"  SPF: {record['spf_result']}, DKIM: {record['dkim_result']}, DMARC: {record['dmarc_result']}")
        print(f"  Behavioral score: {float(record['max_behavioral_sandbox_score']):.4f}")
        print(f"  Exfiltration score: {float(record['max_exfiltration_behavior_score']):.4f}")
        print(f"  DMARC enforced: {record['dmarc_enforced']}")

# Analyze common patterns in No Action records
if no_action_records:
    print(f"\n{'=' * 80}")
    print("PATTERN ANALYSIS OF NO ACTION EMAILS:")
    
    # Calculate averages
    avg_sender_rep = sum(float(r['sender_domain_reputation_score']) for r in no_action_records) / len(no_action_records)
    avg_spam = sum(float(r['content_spam_score']) for r in no_action_records) / len(no_action_records)
    
    print(f"\nAverage sender reputation: {avg_sender_rep:.4f}")
    print(f"Average spam score: {avg_spam:.10f}")
    
    # Check request types
    request_types = [r['request_type'] for r in no_action_records]
    print(f"\nRequest types found: {set(request_types)}")
    
    # Check authentication
    spf_results = [r['spf_result'] for r in no_action_records]
    dkim_results = [r['dkim_result'] for r in no_action_records]
    print(f"\nSPF results: {set(spf_results)}")
    print(f"DKIM results: {set(dkim_results)}")