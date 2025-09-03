#!/usr/bin/env python3
import csv

# Read the CSV file
with open('001.csv', 'r') as f:
    reader = csv.DictReader(f)
    records = list(reader)

# Define criteria for No Action classification
def is_no_action_candidate(record):
    try:
        # Key criteria based on D32 analysis
        sender_reputation = float(record['sender_domain_reputation_score'])
        spam_score = float(record['content_spam_score'])
        temp_email_likelihood = float(record['sender_temp_email_likelihood'])
        malicious_attachment = int(record['malicious_attachment_Count'])
        sender_malicious = int(record['sender_known_malicios'])
        spoof_detected = int(record['sender_spoof_detected'])
        exploit_detected = int(record['any_exploit_pattern_detected'])
        
        # Authentication checks
        spf = record['spf_result']
        dkim = record['dkim_result']
        
        # Request type check
        request_type = record['request_type']
        suspicious_requests = ['bank_detail_update', 'gift_card_request', 'password_reset', 'payment_request']
        
        # Behavioral scores
        behavioral_score = float(record['max_behavioral_sandbox_score'])
        exfiltration_score = float(record['max_exfiltration_behavior_score'])
        
        # Check if meets No Action criteria
        if (sender_reputation > 0.5 and  # Good sender reputation
            spam_score < 0.1 and  # Low spam score
            temp_email_likelihood < 0.1 and  # Not likely temp email
            malicious_attachment == 0 and  # No malicious attachments
            sender_malicious == 0 and  # Not known malicious sender
            spoof_detected == 0 and  # No spoofing detected
            exploit_detected == 0 and  # No exploits
            request_type not in suspicious_requests and  # No suspicious requests
            behavioral_score < 0.3 and  # Low behavioral score
            exfiltration_score < 0.3):  # Low exfiltration score
            return True
            
    except (ValueError, KeyError):
        return False
    
    return False

# Analyze all records
print("Records that should be classified as No Action:")
print("=" * 60)

for record in records:
    record_id = record['Data ']
    current_class = int(record['total_components_detected_malicious'])
    
    if is_no_action_candidate(record):
        # Get key metrics for display
        try:
            sender_rep = float(record['sender_domain_reputation_score'])
            spam = float(record['content_spam_score'])
            request = record['request_type']
            spf = record['spf_result']
            dkim = record['dkim_result']
            
            status = "ALREADY CLASSIFIED" if current_class == 1 else "SHOULD BE NO ACTION"
            
            print(f"\n{record_id} - {status}")
            print(f"  Sender reputation: {sender_rep:.4f}")
            print(f"  Spam score: {spam:.10f}")
            print(f"  Request type: {request}")
            print(f"  SPF: {spf}, DKIM: {dkim}")
            
        except:
            pass

# Count how many additional records should be No Action
no_action_candidates = []
already_classified = []

for record in records:
    record_id = record['Data ']
    current_class = int(record['total_components_detected_malicious'])
    
    if is_no_action_candidate(record):
        if current_class == 0:
            no_action_candidates.append(record_id)
        else:
            already_classified.append(record_id)

print(f"\n{'=' * 60}")
print(f"SUMMARY:")
print(f"Already classified as No Action: {len(already_classified)} records")
print(f"Additional records that should be No Action: {len(no_action_candidates)} records")
print(f"\nNew No Action candidates: {', '.join(no_action_candidates)}")