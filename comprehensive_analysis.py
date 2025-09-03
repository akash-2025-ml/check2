#!/usr/bin/env python3
import csv

# Read the CSV file
with open('001.csv', 'r') as f:
    reader = csv.DictReader(f)
    records = list(reader)

# Define multiple levels of criteria
def analyze_email(record):
    try:
        # Parse key values
        metrics = {
            'sender_reputation': float(record['sender_domain_reputation_score']),
            'spam_score': float(record['content_spam_score']),
            'temp_email_likelihood': float(record['sender_temp_email_likelihood']),
            'malicious_attachment': int(record['malicious_attachment_Count']),
            'sender_malicious': int(record['sender_known_malicios']),
            'spoof_detected': int(record['sender_spoof_detected']),
            'exploit_detected': int(record['any_exploit_pattern_detected']),
            'behavioral_score': float(record['max_behavioral_sandbox_score']),
            'exfiltration_score': float(record['max_exfiltration_behavior_score']),
            'amsi_suspicion': float(record['max_amsi_suspicion_score']),
            'urgency_keywords': int(record['urgency_keywords_present']),
            'user_marked_spam': int(record['user_marked_as_spam_before']),
            'request_type': record['request_type'],
            'spf': record['spf_result'],
            'dkim': record['dkim_result'],
            'dmarc': record['dmarc_result']
        }
        return metrics
    except:
        return None

# Suspicious request types
suspicious_requests = ['bank_detail_update', 'gift_card_request', 'password_reset', 'payment_request', 'document_download']

print("COMPREHENSIVE ANALYSIS - Potential No Action Emails")
print("=" * 80)

# Strict criteria (high confidence)
print("\n1. HIGH CONFIDENCE - No Action candidates:")
print("   Criteria: reputation>0.5, spam<0.1, no malicious indicators, no suspicious requests")
print("-" * 80)

high_confidence = []
for record in records:
    metrics = analyze_email(record)
    if not metrics:
        continue
        
    if (metrics['sender_reputation'] > 0.5 and
        metrics['spam_score'] < 0.1 and
        metrics['temp_email_likelihood'] < 0.1 and
        metrics['malicious_attachment'] == 0 and
        metrics['sender_malicious'] == 0 and
        metrics['spoof_detected'] == 0 and
        metrics['exploit_detected'] == 0 and
        metrics['request_type'] not in suspicious_requests and
        metrics['behavioral_score'] < 0.2 and
        metrics['exfiltration_score'] < 0.2 and
        metrics['amsi_suspicion'] < 0.1 and
        metrics['urgency_keywords'] == 0 and
        metrics['user_marked_spam'] == 0):
        
        record_id = record['Data ']
        current_class = int(record['total_components_detected_malicious'])
        high_confidence.append(record_id)
        print(f"{record_id} (class={current_class}): rep={metrics['sender_reputation']:.3f}, spam={metrics['spam_score']:.6f}, request={metrics['request_type']}")

# Medium confidence
print(f"\n2. MEDIUM CONFIDENCE - No Action candidates:")
print("   Criteria: reputation>0.3, spam<0.2, low risk indicators")
print("-" * 80)

medium_confidence = []
for record in records:
    metrics = analyze_email(record)
    if not metrics:
        continue
        
    record_id = record['Data ']
    if record_id in high_confidence:
        continue
        
    if (metrics['sender_reputation'] > 0.3 and
        metrics['spam_score'] < 0.2 and
        metrics['malicious_attachment'] == 0 and
        metrics['sender_malicious'] == 0 and
        metrics['exploit_detected'] == 0 and
        metrics['request_type'] not in ['bank_detail_update', 'gift_card_request', 'password_reset'] and
        metrics['behavioral_score'] < 0.3 and
        metrics['exfiltration_score'] < 0.3 and
        metrics['amsi_suspicion'] < 0.2):
        
        current_class = int(record['total_components_detected_malicious'])
        medium_confidence.append(record_id)
        print(f"{record_id} (class={current_class}): rep={metrics['sender_reputation']:.3f}, spam={metrics['spam_score']:.6f}, request={metrics['request_type']}")

# Authentication-based analysis
print(f"\n3. AUTHENTICATION ANALYSIS - Good authentication emails:")
print("   Looking for pass/valid authentication results")
print("-" * 80)

good_auth = []
for record in records:
    metrics = analyze_email(record)
    if not metrics:
        continue
        
    record_id = record['Data ']
    current_class = int(record['total_components_detected_malicious'])
    
    # Count good authentication
    auth_score = 0
    if metrics['spf'] == 'pass':
        auth_score += 1
    if metrics['dkim'] == 'pass':
        auth_score += 1
    if metrics['dmarc'] == 'pass':
        auth_score += 1
        
    if auth_score >= 2:  # At least 2 out of 3 pass
        good_auth.append(record_id)
        print(f"{record_id} (class={current_class}): SPF={metrics['spf']}, DKIM={metrics['dkim']}, DMARC={metrics['dmarc']}, rep={metrics['sender_reputation']:.3f}")

# Final summary
print(f"\n{'=' * 80}")
print("FINAL RECOMMENDATIONS FOR NO ACTION CLASSIFICATION:")
print(f"\nHigh confidence (should definitely be No Action): {', '.join(high_confidence) if high_confidence else 'None found'}")
print(f"\nMedium confidence (likely No Action): {', '.join(medium_confidence) if medium_confidence else 'None found'}")
print(f"\nGood authentication (consider for No Action): {', '.join(good_auth) if good_auth else 'None found'}")

# Look for patterns in current class=1 emails to understand the classification
print(f"\n{'=' * 80}")
print("UNDERSTANDING CURRENT CLASSIFICATION:")
current_no_action = [r['Data '] for r in records if int(r['total_components_detected_malicious']) == 1]
print(f"Currently classified as 1: {', '.join(current_no_action)}")

# Check if D32 really should be No Action
print(f"\n{'=' * 80}")
print("DETAILED ANALYSIS OF D32:")
for record in records:
    if record['Data '] == 'D32':
        metrics = analyze_email(record)
        if metrics:
            print(f"Sender reputation: {metrics['sender_reputation']:.4f} (GOOD)")
            print(f"Spam score: {metrics['spam_score']:.10f} (VERY LOW)")
            print(f"Request type: {metrics['request_type']} (NONE - not suspicious)")
            print(f"No malicious indicators: malicious={metrics['sender_malicious']}, spoof={metrics['spoof_detected']}, exploit={metrics['exploit_detected']}")
            print(f"Low risk scores: behavioral={metrics['behavioral_score']:.3f}, exfiltration={metrics['exfiltration_score']:.3f}")
            print(f"Authentication: SPF={metrics['spf']}, DKIM={metrics['dkim']}, DMARC={metrics['dmarc']}")
            print("\nCONCLUSION: D32 shows strong indicators of being a legitimate email")