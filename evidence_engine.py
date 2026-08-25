import re

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Evidence:
    text: str
    weight: float
    source: str

def score_evidence(case: Dict):
    out = case.get("show_outputs", "")
    fault = case.get("expected_fault", "")
    tokens = set(re.findall(r"[a-zA-Z0-9./_-]+", (out + " " + fault).lower()))
    fault_tokens = set(re.findall(r"[a-zA-Z0-9./_-]+", fault.lower()))
    overlap = len(tokens & fault_tokens)
    confidence = min(0.98, 0.55 + overlap * 0.035)
    return round(confidence, 2)

def contradiction_scan(case: Dict):
    text = (case.get("show_outputs","") + " " + case.get("topology_note","")).lower()
    contradictions = []
    if "up up" in text and "administratively down" in text:
        contradictions.append("Mixed interface-state evidence: verify the exact interface before changing configuration.")
    if "permit ip any any" in text and "guest" in text:
        contradictions.append("Guest isolation policy appears inconsistent with an unrestricted permit.")
    return contradictions

def command_risk(commands):
    high_risk = ["reload", "erase", "write erase", "default interface", "shutdown"]
    score = 10
    reasons = []
    for cmd in commands:
        c = cmd.lower()
        if any(x in c for x in high_risk):
            score += 25
            reasons.append(f"Potentially disruptive command: {cmd}")
        elif c.startswith(("no ", "ip ", "switchport ", "router ", "access-list")):
            score += 5
    score = min(score, 100)
    label = "Low" if score < 35 else "Medium" if score < 65 else "High"
    return {"score": score, "label": label, "reasons": reasons}

def build_evidence_graph(case, findings):
    nodes = [
        {"id":"S","label":"Symptom","value":case["symptom"]},
        {"id":"T","label":"Topology","value":case["topology_note"]},
        {"id":"O","label":"Show Output","value":case["show_outputs"]},
        {"id":"F","label":"Expected Fault","value":case["expected_fault"]},
    ]
    edges = [
        {"from":"S","to":"O","relation":"supported by"},
        {"from":"T","to":"O","relation":"contextualizes"},
        {"from":"O","to":"F","relation":"evidence for"},
    ]
    return {"nodes":nodes,"edges":edges}
