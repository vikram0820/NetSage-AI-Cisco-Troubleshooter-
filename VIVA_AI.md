# Viva: Real AI Integration

**Q: Which AI model is used?**
Google Gemini via the official `google-genai` Python SDK.

**Q: Is the AI actually generating the diagnosis?**
Yes. The "Run Gemini AI Diagnosis" button sends the selected case's symptom, topology note and show-command evidence to Gemini and receives a structured JSON diagnosis.

**Q: Why JSON?**
The project requirement asks for structured fields such as root cause, confidence, evidence, next command and fix steps. Gemini supports structured JSON output using a response schema.

**Q: Is the AI allowed to execute commands?**
No. It only proposes commands. Human review is mandatory.

**Q: What happens if Gemini is wrong?**
The deterministic checker, evidence/contradiction checks and human Accept/Edit/Reject gate provide additional safeguards and auditability.

**Q: Is the API key stored in code?**
No. It is read from `GEMINI_API_KEY`.
