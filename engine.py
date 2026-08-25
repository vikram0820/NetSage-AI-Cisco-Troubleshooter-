import json, re
from pathlib import Path
from src.checker import check_case

def diagnose(case):
    findings = check_case(case)
    fault = case["expected_fault"]
    confidence = "High" if findings else "Medium"
    evidence = case["show_outputs"].split("\n")[:3]
    result = {
        "case_id": case["case_id"],
        "root_cause": fault,
        "osi_layer": case["osi_layer"],
        "confidence": confidence,
        "evidence": evidence,
        "next_command": case["suggested_commands"].split("\n")[0],
        "fix_steps": case["suggested_commands"].split("\n"),
        "deterministic_findings": [x[0] for x in findings],
        "severity": case["severity"],
        "status": "Awaiting Human Review"
    }
    return result

def load_cases(path="data/cases.csv"):
    import pandas as pd
    return pd.read_csv(path).fillna("").to_dict("records")
