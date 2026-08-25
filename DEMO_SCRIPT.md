# 5–7 Minute Demo Script

## 1. Problem (30 sec)
"Junior engineers can know commands but still struggle to connect symptoms to root cause. NetSage AI combines deterministic checks with AI-style structured diagnosis and mandatory human review."

## 2. Open dashboard (30 sec)
Show the 30 cases and issue families.

## 3. NET-001 diagnosis (2 min)
Select NET-001. Explain:
- PC cannot reach Server1 in VLAN 30.
- show output says Gi0/0.30 is administratively down.
- Rule engine flags the interface.
- Diagnosis identifies Layer 3 inter-VLAN issue.
- Proposed fix is `no shutdown`.

## 4. Evidence + safety (1 min)
Open Evidence Graph and Command Safety.
Explain that the system does not blindly trust generated commands.

## 5. Human review (1 min)
Edit/accept/reject the fix. Explain that approval is mandatory and the decision is logged.

## 6. Audit (1 min)
Show the 5 responsible-AI correction examples and current session investigation ID.

## Closing
"NetSage AI is not just a chatbot. It is a safety-oriented diagnostic workflow that combines rules, evidence, explainability, command-risk analysis, human review and auditability."
