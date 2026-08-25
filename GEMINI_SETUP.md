# Gemini Free API Setup

## 1. Create the key
Open Google AI Studio API Keys and create an API key.

## 2. Install
```bash
pip install -r requirements.txt
```

## 3. Set the key

### Windows PowerShell
```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
$env:NETSAGE_MODEL="gemini-2.5-flash-lite"
streamlit run app.py
```

### Windows CMD
```cmd
set GEMINI_API_KEY=YOUR_KEY
set NETSAGE_MODEL=gemini-2.5-flash-lite
streamlit run app.py
```

### Linux/macOS
```bash
export GEMINI_API_KEY="YOUR_KEY"
export NETSAGE_MODEL="gemini-2.5-flash-lite"
streamlit run app.py
```

Do NOT put the real API key into the source code or commit it to GitHub.

## What happens in the app
Select a case → Run Gemini AI Diagnosis → Gemini returns strict JSON → local evidence/risk checks run → human can Accept/Edit/Reject.

The application never executes Cisco CLI commands automatically.
