# check2

Prompt 1:
 
You are a Senior Email Security Analyst. Your task is to classify emails into one of four categories: Malicious, Spam, Warning, or No Action.
You are provided with three reference files:
@Detection_Signals_Essentials_1.0.csv → Contains details of all 68 detection signals, including whether higher or lower values are good (from the Type Explanation column) and further information in the Detailed Descriptioncolumn.
@base_document.txt → Contains the definitions and rules for the four classifications (Malicious, Spam, Warning, No Action).
@30Data.csv → Contains the generated detection signal values for 30 emails (Data ID + 68 signal values).
 
Instructions:
Carefully analyze all 68 detection signals for each email.
Apply the  definion in @base_document.txt consistently.
Classification must be accurate and mission-critical.
For the first 5 emails (Data IDs 1–5), classify them and export results to outcome.csv in the format: [Data ID],[Classification]
 
Prompt 2:
Repeat the same process for the next 5 emails from @30Data.csv and append results to outcome.csv in the same format.
 
Prompt 3:
Repeat the same process for the next 5 emails from @30Data.csv and append results to outcome.csv in the same format.
