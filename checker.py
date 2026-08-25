import re

def check_case(case):
    text = (case.get("show_outputs","") + "\n" + case.get("symptom","")).lower()
    findings = []
    if "administratively down" in text or "shutdown" in text:
        findings.append(("Interface/SVI is administratively down", "High"))
    if "missing" in text and "vlan" in text or "no vlan" in text:
        findings.append(("VLAN may be missing", "High"))
    if "allowed" in text and "vlan 30" in text and "10,20" in text:
        findings.append(("Required VLAN is missing from trunk allowed list", "High"))
    if "permit ip any any" in text and "guest" in text:
        findings.append(("Guest ACL appears overly permissive", "Critical"))
    if "deny icmp" in text:
        findings.append(("ACL explicitly denies ICMP", "High"))
    if "no route" in text or "missing route" in text:
        findings.append(("Routing information appears incomplete", "High"))
    if "duplicate ip" in text or "same address" in text:
        findings.append(("Possible duplicate IP address", "High"))
    if "169.254" in text or "dhcp" in text and ("wrong" in text or "missing" in text):
        findings.append(("DHCP configuration/lease issue suspected", "High"))
    if "dns" in text and ("incorrect" in text or "nxdomain" in text):
        findings.append(("DNS configuration/resolution issue suspected", "Medium"))
    if "nat" in text and ("empty" in text or "missing" in text or "reversed" in text):
        findings.append(("NAT/PAT configuration issue suspected", "High"))
    if "area" in text and "ospf" in text:
        findings.append(("OSPF area/configuration mismatch suspected", "High"))
    if "access" in text and "trunk" in text and "static access" in text:
        findings.append(("Trunk port is operating as access mode", "High"))
    if "wildcard" in text:
        findings.append(("ACL wildcard mask issue suspected", "High"))
    if "native vlan" in text:
        findings.append(("Native VLAN mismatch suspected", "Medium"))
    if "port-security" in text or "violation" in text:
        findings.append(("Port-security violation suspected", "High"))
    return findings
