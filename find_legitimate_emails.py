#!/usr/bin/env python3
import csv

# Read the CSV file
with open('001.csv', 'r') as f:
    reader = csv.DictReader(f)
    records = list(reader)

# Define criteria for legitimate "No Action" emails
def is_legitimate_email(record):
    try:
        # Parse key values
        sender_reputation = float(record['sender_domain_reputation_score'])
        spam_score = float(record['content_spam_score'])
        temp_email_likelihood = float(record['sender_temp_email_likelihood'])
        malicious_attachment = int(record['malicious_attachment_Count'])
        sender_malicious = int(record['sender_known_malicios'])
        spoof_detected = int(record['sender_spoof_detected'])
        exploit_detected = int(record['any_exploit_pattern_detected'])
        behavioral_score = float(record['max_behavioral_sandbox_score'])
        exfiltration_score = float(record['max_exfiltration_behavior_score'])
        amsi_suspicion = float(record['max_amsi_suspicion_score'])
        
        # Request type check
        request_type = record['request_type']
        suspicious_requests = ['bank_detail_update', 'gift_card_request', 'password_reset', 'payment_request']
        
        # Check if meets legitimate criteria
        if (sender_reputation > 0.5 and  # Good sender reputation
            spam_score < 0.1 and  # Low spam score
            temp_email_likelihood < 0.1 and  # Not likely temp email
            malicious_attachment == 0 and  # No malicious attachments
            sender_malicious == 0 and  # Not known malicious sender
            spoof_detected == 0 and  # No spoofing detected
            exploit_detected == 0 and  # No exploits
            request_type not in suspicious_requests and  # No suspicious requests
            behavioral_score < 0.2 and  # Low behavioral score
            exfiltration_score < 0.2 and  # Low exfiltration score
            amsi_suspicion < 0.1):  # Low AMSI suspicion
            return True
            
    except (ValueError, KeyError):
        return False
    
    return False

# Analyze all records
print("Records that match No Action criteria (legitimate, expected, relevant emails):")
print("=" * 80)

legitimate_emails = []
for record in records:
    record_id = record['Data ']
    current_class = int(record['total_components_detected_malicious'])
    
    if is_legitimate_email(record):
        legitimate_emails.append(record)
        print(f"\n{record_id} (Currently classified as: {current_class}):")
        print(f"  Sender reputation: {float(record['sender_domain_reputation_score']):.4f}")
        print(f"  Spam score: {float(record['content_spam_score']):.10f}")
        print(f"  Temp email likelihood: {float(record['sender_temp_email_likelihood']):.4f}")
        print(f"  Request type: {record['request_type']}")
        print(f"  SPF: {record['spf_result']}, DKIM: {record['dkim_result']}, DMARC: {record['dmarc_result']}")
        print(f"  Behavioral score: {float(record['max_behavioral_sandbox_score']):.4f}")
        print(f"  Exfiltration score: {float(record['max_exfiltration_behavior_score']):.4f}")
        print(f"  AMSI suspicion: {float(record['max_amsi_suspicion_score']):.4f}")
        print(f"  URL reputation: {record['url_reputation_score']}")
        print(f"  SSL validity: {record['ssl_validity_status']}")

print(f"\n{'=' * 80}")
print(f"SUMMARY: Found {len(legitimate_emails)} emails that match No Action criteria")

# Group by current classification
by_class = {}
for record in legitimate_emails:
    current_class = int(record['total_components_detected_malicious'])
    record_id = record['Data ']
    if current_class not in by_class:
        by_class[current_class] = []
    by_class[current_class].append(record_id)

print("\nGrouped by current classification:")
for class_val, records_list in sorted(by_class.items()):
    print(f"  Class {class_val}: {', '.join(records_list)}")

# Additional analysis - look for borderline cases
print(f"\n{'=' * 80}")
print("Borderline cases (sender reputation 0.4-0.5):")
for record in records:
    try:
        sender_rep = float(record['sender_domain_reputation_score'])
        if 0.4 <= sender_rep <= 0.5:
            record_id = record['Data ']
            spam = float(record['content_spam_score'])
            request = record['request_type']
            current_class = int(record['total_components_detected_malicious'])
            print(f"{record_id}: reputation={sender_rep:.4f}, spam={spam:.6f}, request={request}, class={current_class}")
    except:
        pass