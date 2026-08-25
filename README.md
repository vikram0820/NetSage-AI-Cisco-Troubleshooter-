# NetSage AI — Cisco Network Diagnostic Intelligence

AI-assisted Cisco troubleshooting dashboard with:
- Real Google Gemini diagnosis
- Deterministic Cisco rule checks
- Evidence scoring and contradiction detection
- Command-risk analysis
- Human Accept / Edit / Reject gate
- Responsible-AI audit trail
- Streamlit dashboard

## Run on Windows

### First time
Double-click:
`SETUP_NETSAGE.bat`

Enter your Gemini API key when asked.

### Every next time
Double-click:
`START_NETSAGE.bat`

No repeated API key/model commands are required.

## Security
Your `.env` file contains the API key and is ignored by Git via `.gitignore`. Never upload `.env` to GitHub.

## GitHub
Upload all project files EXCEPT `.env`.
The repository can safely contain `.env.example`.
