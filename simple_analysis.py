#!/usr/bin/env python3
import csv

# Read the CSV file
with open('001.csv', 'r') as f:
    reader = csv.DictReader(f)
    records = list(reader)

print("ANALYSIS: Finding emails that match No Action definition")
print("No Action = Messages that are legitimate, expected, and relevant to the recipient")
print("=" * 100)

# Check each record
candidates = []
for record in records:
    try:
        record_id = record['Data '].strip()
        current_class = int(record['total_components_detected_malicious'])
        
        # Key metrics
        sender_rep = float(record['sender_domain_reputation_score'])
        spam_score = float(record['content_spam_score'])
        temp_email = float(record['sender_temp_email_likelihood'])
        request_type = record['request_type'].strip()
        spf = record['spf_result'].strip()
        dkim = record['dkim_result'].strip()
        
        # Malicious indicators
        sender_malicious = int(record['sender_known_malicios'])
        spoof = int(record['sender_spoof_detected'])
        malicious_attach = int(record['malicious_attachment_Count'])
        exploit = int(record['any_exploit_pattern_detected'])
        
        # Behavioral scores
        behavioral = float(record['max_behavioral_sandbox_score'])
        exfiltration = float(record['max_exfiltration_behavior_score'])
        amsi = float(record['max_amsi_suspicion_score'])
        
        # Check if record has good characteristics
        is_good = True
        reasons = []
        
        # Must have no malicious indicators
        if sender_malicious > 0 or spoof > 0 or malicious_attach > 0 or exploit > 0:
            is_good = False
            continue
            
        # Check sender reputation
        if sender_rep > 0.5:
            reasons.append(f"Good sender reputation ({sender_rep:.3f})")
        elif sender_rep > 0.3:
            reasons.append(f"Fair sender reputation ({sender_rep:.3f})")
        else:
            continue  # Skip low reputation
            
        # Check spam score
        if spam_score < 0.01:
            reasons.append(f"Very low spam score ({spam_score:.6f})")
        elif spam_score < 0.1:
            reasons.append(f"Low spam score ({spam_score:.6f})")
        else:
            continue  # Skip high spam scores
            
        # Check request type
        suspicious_requests = ['bank_detail_update', 'gift_card_request', 'password_reset', 'payment_request']
        if request_type in suspicious_requests:
            continue  # Skip suspicious requests
        elif request_type == 'none':
            reasons.append("No suspicious request type")
        else:
            reasons.append(f"Request type: {request_type}")
            
        # Check behavioral scores
        if behavioral < 0.2 and exfiltration < 0.2 and amsi < 0.1:
            reasons.append("Low behavioral risk scores")
        else:
            continue  # Skip high risk scores
            
        # If we got here, it's a candidate
        candidates.append({
            'id': record_id,
            'class': current_class,
            'reputation': sender_rep,
            'spam': spam_score,
            'reasons': reasons,
            'spf': spf,
            'dkim': dkim
        })
        
    except Exception as e:
        continue

# Sort by reputation
candidates.sort(key=lambda x: x['reputation'], reverse=True)

# Display results
print("\nEMAILS THAT SHOULD BE CLASSIFIED AS NO ACTION:")
print("-" * 100)

for candidate in candidates:
    status = "ALREADY CLASSIFIED AS 1" if candidate['class'] == 1 else "SHOULD BE NO ACTION"
    print(f"\n{candidate['id']} - {status}")
    print(f"  Current classification: {candidate['class']}")
    print(f"  Reputation: {candidate['reputation']:.4f}, Spam: {candidate['spam']:.6f}")
    print(f"  SPF: {candidate['spf']}, DKIM: {candidate['dkim']}")
    print(f"  Reasons: {'; '.join(candidate['reasons'])}")

# Summary
print(f"\n{'=' * 100}")
print("SUMMARY:")
should_be_no_action = [c['id'] for c in candidates if c['class'] != 1]
already_no_action = [c['id'] for c in candidates if c['class'] == 1]

print(f"\nRecords that SHOULD BE reclassified as No Action: {', '.join(should_be_no_action) if should_be_no_action else 'None'}")
print(f"Records already classified as 1 that match criteria: {', '.join(already_no_action) if already_no_action else 'None'}")

# Additional check - what's special about current class 1 emails?
print(f"\n{'=' * 100}")
print("CURRENT CLASS 1 EMAILS ANALYSIS:")
for record in records:
    if int(record['total_components_detected_malicious']) == 1:
        record_id = record['Data '].strip()
        sender_rep = float(record['sender_domain_reputation_score'])
        spam_score = float(record['content_spam_score'])
        request_type = record['request_type'].strip()
        print(f"{record_id}: reputation={sender_rep:.3f}, spam={spam_score:.3f}, request={request_type}")