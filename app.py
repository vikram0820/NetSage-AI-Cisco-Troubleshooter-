
import streamlit as st
import pandas as pd
import hashlib, datetime, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from src.engine import diagnose
from src.gemini_provider import ai_available, ai_diagnose
from src.checker import check_case
from src.evidence_engine import score_evidence, contradiction_scan, command_risk, build_evidence_graph

st.set_page_config(
    page_title="NetSage AI",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PREMIUM UI ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 15% 0%, rgba(99,102,241,.14), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(14,165,233,.12), transparent 25%),
        #070b14;
}

[data-testid="stHeader"] {
    background: rgba(7,11,20,.75);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1020 0%, #080c16 100%);
    border-right: 1px solid rgba(148,163,184,.14);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

.hero {
    padding: 28px 30px;
    border: 1px solid rgba(129,140,248,.25);
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(30,41,90,.82), rgba(9,15,29,.94));
    box-shadow: 0 20px 60px rgba(0,0,0,.28);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 2.25rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
}

.hero-sub {
    color: #aab5c7;
    margin-top: 8px;
    font-size: .98rem;
}

.pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 700;
    margin-right: 7px;
    border: 1px solid rgba(255,255,255,.12);
}

.pill-green { background: rgba(34,197,94,.12); color:#86efac; }
.pill-blue { background: rgba(59,130,246,.12); color:#93c5fd; }
.pill-purple { background: rgba(139,92,246,.12); color:#c4b5fd; }

.section-title {
    font-size: 1.25rem;
    font-weight: 750;
    margin: 20px 0 10px;
}

.card {
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(148,163,184,.14);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 10px 35px rgba(0,0,0,.16);
    height: 100%;
}

.card-title {
    font-size: .82rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #94a3b8;
    font-weight: 700;
}

.card-value {
    font-size: 1.35rem;
    font-weight: 750;
    margin-top: 7px;
    color: #f8fafc;
}

.status-online {
    display:flex;
    align-items:center;
    gap:8px;
    padding:10px 12px;
    border-radius:12px;
    background:rgba(34,197,94,.08);
    border:1px solid rgba(34,197,94,.20);
    color:#86efac;
    font-weight:700;
}

.status-offline {
    display:flex;
    align-items:center;
    gap:8px;
    padding:10px 12px;
    border-radius:12px;
    background:rgba(245,158,11,.08);
    border:1px solid rgba(245,158,11,.20);
    color:#fcd34d;
    font-weight:700;
}

.root-card {
    border: 1px solid rgba(34,197,94,.22);
    background: linear-gradient(135deg, rgba(22,101,52,.22), rgba(15,23,42,.78));
    border-radius: 20px;
    padding: 22px;
}

.root-label {
    color:#86efac;
    font-weight:800;
    font-size:.78rem;
    text-transform:uppercase;
    letter-spacing:.08em;
}

.root-text {
    font-size:1.2rem;
    line-height:1.55;
    font-weight:650;
    margin-top:8px;
}

.evidence-item {
    padding: 12px 14px;
    border-left: 3px solid #818cf8;
    background: rgba(99,102,241,.07);
    border-radius: 0 12px 12px 0;
    margin-bottom: 9px;
}

.risk-low { color:#86efac; }
.risk-medium { color:#fcd34d; }
.risk-high { color:#fca5a5; }

div[data-testid="stMetric"] {
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(148,163,184,.14);
    padding: 14px;
    border-radius: 16px;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
    border: 1px solid rgba(148,163,184,.18);
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border: none;
}

.stCodeBlock {
    border-radius: 14px !important;
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
cases = pd.read_csv(Path(__file__).parent / "data" / "cases.csv").fillna("")

if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🛰️ NetSage AI")
    st.caption("Cisco Network Diagnostic Intelligence")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "🧠 Live Diagnosis",
            "🗺️ Evidence Graph",
            "🛡️ Command Safety",
            "📊 Intelligence Analytics",
            "📜 Audit Trail",
            "ℹ️ Architecture"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    if ai_available():
        st.markdown('<div class="status-online">● Gemini AI Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">● Gemini Offline / Demo</div>', unsafe_allow_html=True)

    st.markdown("### System Snapshot")
    st.metric("Diagnostic Cases", len(cases))
    st.metric("Concept Families", cases["concept_tag"].nunique())
    st.metric("High / Critical", int(cases["severity"].isin(["High", "Critical"]).sum()))

    st.divider()
    st.caption("Human approval is required before accepting remediation.")

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <div>
        <span class="pill pill-purple">AI-ASSISTED</span>
        <span class="pill pill-blue">EVIDENCE-GROUNDED</span>
        <span class="pill pill-green">HUMAN-IN-THE-LOOP</span>
    </div>
    <div class="hero-title">NetSage AI</div>
    <div class="hero-sub">
        Intelligent Cisco troubleshooting with deterministic verification,
        Gemini reasoning, command-risk analysis and explainable evidence.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- LIVE DIAGNOSIS ----------
if page == "🧠 Live Diagnosis":
    st.markdown('<div class="section-title">Live Incident Investigation</div>', unsafe_allow_html=True)

    top1, top2, top3 = st.columns([2.2, 1, 1])
    with top1:
        selected = st.selectbox(
            "Select Packet Tracer Incident",
            cases["case_id"].tolist(),
            label_visibility="collapsed"
        )
    case = cases[cases.case_id == selected].iloc[0].to_dict()

    with top2:
        st.metric("Severity", case["severity"])
    with top3:
        st.metric("Concept", case["concept_tag"])

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="section-title">🚨 Incident</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Symptom</div>
            <div style="font-size:1.1rem;font-weight:650;margin-top:8px">{case["symptom"]}</div>
            <br>
            <div class="card-title">Topology Context</div>
            <div style="color:#cbd5e1;margin-top:7px">{case["topology_note"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">🔎 Evidence Capture</div>', unsafe_allow_html=True)
        st.code(case["show_outputs"], language="text")

    b1, b2 = st.columns([1.6, 1])
    with b1:
        run_ai = st.button("🤖  Run Gemini AI Diagnosis", type="primary", use_container_width=True)
    with b2:
        run_rules = st.button("⚙️  Run Rule Engine", use_container_width=True)

    if run_ai:
        if not ai_available():
            st.warning("Gemini is not connected. Set GEMINI_API_KEY and restart Streamlit.")
        else:
            with st.spinner("NetSage AI is analyzing evidence..."):
                try:
                    ai_result = ai_diagnose(case)
                    ai_result["case_id"] = selected
                    ai_result["ai_source"] = "Google Gemini"
                    ai_result["evidence_score"] = score_evidence(case)
                    ai_result["contradictions"] = contradiction_scan(case)
                    ai_result["command_safety"] = command_risk(ai_result.get("fix_steps", []))
                    ai_result["deterministic_findings"] = [x[0] for x in check_case(case)]
                    ai_result["investigation_id"] = hashlib.sha256(
                        f'GEMINI-{selected}-{datetime.datetime.now().isoformat()}'.encode()
                    ).hexdigest()[:12].upper()
                    ai_result["review_state"] = "PENDING HUMAN REVIEW"
                    st.session_state.result = ai_result
                except Exception as e:
                    st.error(f"Gemini API error: {e}")

    if run_rules:
        result = diagnose(case)
        result["evidence_score"] = score_evidence(case)
        result["contradictions"] = contradiction_scan(case)
        result["command_safety"] = command_risk(result["fix_steps"])
        result["investigation_id"] = hashlib.sha256(
            f'{selected}-{datetime.datetime.now().isoformat()}'.encode()
        ).hexdigest()[:12].upper()
        result["review_state"] = "PENDING HUMAN REVIEW"
        st.session_state.result = result

    r = st.session_state.result

    if r and r.get("case_id") == selected:
        st.divider()

        source = "REAL GEMINI" if r.get("ai_source") == "Google Gemini" else "DETERMINISTIC ENGINE"
        st.markdown(
            f'<span class="pill pill-purple">{source}</span> '
            f'<span class="pill pill-blue">INVESTIGATION {r["investigation_id"]}</span>',
            unsafe_allow_html=True
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("OSI Layer", r.get("osi_layer", "—"))
        m2.metric("Evidence Confidence", f'{r.get("evidence_score", 0):.0%}')
        m3.metric("Command Risk", r.get("command_safety", {}).get("label", "—"))
        m4.metric("Human Review", "REQUIRED")

        st.markdown('<div class="section-title">🎯 Root Cause</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="root-card"><div class="root-label">Most Likely Root Cause</div>'
            f'<div class="root-text">{r.get("root_cause","No diagnosis returned.")}</div></div>',
            unsafe_allow_html=True
        )

        ev_col, cmd_col = st.columns([1.15, .85], gap="large")

        with ev_col:
            st.markdown('<div class="section-title">🔬 Evidence Chain</div>', unsafe_allow_html=True)
            for e in r.get("evidence", []):
                st.markdown(f'<div class="evidence-item">↳ {e}</div>', unsafe_allow_html=True)

            findings = r.get("deterministic_findings", [])
            if findings:
                st.markdown('<div class="section-title">🧩 Rule Engine Findings</div>', unsafe_allow_html=True)
                for item in findings:
                    st.warning(item)

            contradictions = r.get("contradictions", [])
            if contradictions:
                st.markdown('<div class="section-title">⚠️ Contradiction Detector</div>', unsafe_allow_html=True)
                for c in contradictions:
                    st.error(c)

        with cmd_col:
            st.markdown('<div class="section-title">🧭 Next Diagnostic Command</div>', unsafe_allow_html=True)
            st.code(r.get("next_command", ""), language="text")

            st.markdown('<div class="section-title">🛡️ Proposed Remediation</div>', unsafe_allow_html=True)
            edited = st.text_area(
                "Human reviewer can edit before approval",
                "\n".join(r.get("fix_steps", [])),
                height=180,
                label_visibility="collapsed"
            )

            risk = r.get("command_safety", {})
            label = risk.get("label", "Unknown")
            if label == "Low":
                st.markdown(f'<b class="risk-low">● Low command risk</b>', unsafe_allow_html=True)
            elif label == "Medium":
                st.markdown(f'<b class="risk-medium">● Medium command risk</b>', unsafe_allow_html=True)
            else:
                st.markdown(f'<b class="risk-high">● High command risk</b>', unsafe_allow_html=True)

            for reason in risk.get("reasons", []):
                st.warning(reason)

        st.divider()
        st.markdown('<div class="section-title">👤 Human Decision Gate</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        if c1.button("✅ ACCEPT", use_container_width=True):
            st.session_state.history.append([r["investigation_id"], selected, "ACCEPTED", edited])
            st.success("Accepted. No live Cisco device is touched.")
        if c2.button("✏️ EDIT + ACCEPT", use_container_width=True):
            st.session_state.history.append([r["investigation_id"], selected, "EDITED", edited])
            st.success("Edited remediation recorded.")
        if c3.button("❌ REJECT", use_container_width=True):
            st.session_state.history.append([r["investigation_id"], selected, "REJECTED", edited])
            st.error("Rejected and added to the audit trail.")

        with st.expander("View Machine-Readable Diagnostic JSON"):
            st.json(r)

# ---------- EVIDENCE GRAPH ----------
elif page == "🗺️ Evidence Graph":
    st.markdown('<div class="section-title">🗺️ Explainable Evidence Graph</div>', unsafe_allow_html=True)
    selected = st.selectbox("Incident", cases["case_id"].tolist(), key="graph_case")
    case = cases[cases.case_id == selected].iloc[0].to_dict()
    findings = check_case(case)
    graph = build_evidence_graph(case, findings)

    st.info("Reasoning chain: Symptom → Topology → Show Output → Expected Fault.")

    cols = st.columns(len(graph["nodes"]))
    for col, node in zip(cols, graph["nodes"]):
        with col:
            st.markdown(
                f'<div class="card"><div class="card-title">{node["label"]}</div>'
                f'<div style="margin-top:8px;color:#cbd5e1">{node["value"]}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">Relationship Map</div>', unsafe_allow_html=True)
    for edge in graph["edges"]:
        st.markdown(f"**{edge['from']}** → *{edge['relation']}* → **{edge['to']}**")

# ---------- COMMAND SAFETY ----------
elif page == "🛡️ Command Safety":
    st.markdown('<div class="section-title">🛡️ Command Safety Gate</div>', unsafe_allow_html=True)
    st.caption("Every proposed CLI action is scored before a human can approve it.")

    selected = st.selectbox("Incident", cases["case_id"].tolist(), key="risk_case")
    case = cases[cases.case_id == selected].iloc[0].to_dict()
    r = diagnose(case)
    risk = command_risk(r["fix_steps"])

    a,b,c = st.columns(3)
    a.metric("Risk Score", f'{risk["score"]}/100')
    b.metric("Risk Level", risk["label"])
    c.metric("Commands", len(r["fix_steps"]))

    st.markdown('<div class="section-title">Proposed CLI</div>', unsafe_allow_html=True)
    st.code("\n".join(r["fix_steps"]), language="text")

    if risk["reasons"]:
        for reason in risk["reasons"]:
            st.warning(reason)
    else:
        st.success("No high-risk command pattern detected in this lab remediation.")

    st.info("Safety design: NetSage AI proposes commands only. It does not automatically configure a real Cisco device.")

# ---------- ANALYTICS ----------
elif page == "📊 Intelligence Analytics":
    st.markdown('<div class="section-title">📊 Network Intelligence</div>', unsafe_allow_html=True)

    a,b,c,d = st.columns(4)
    a.metric("Total Cases", len(cases))
    b.metric("Concepts", cases["concept_tag"].nunique())
    c.metric("High", int((cases["severity"]=="High").sum()))
    d.metric("Critical", int((cases["severity"]=="Critical").sum()))

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("#### Fault Family Distribution")
        st.bar_chart(cases["concept_tag"].value_counts())
    with right:
        st.markdown("#### Severity Distribution")
        st.bar_chart(cases["severity"].value_counts())

    st.markdown("#### Case Explorer")
    st.dataframe(
        cases[["case_id","concept_tag","severity","symptom","expected_fault"]],
        use_container_width=True,
        hide_index=True
    )

# ---------- AUDIT ----------
elif page == "📜 Audit Trail":
    st.markdown('<div class="section-title">📜 Human Oversight & Audit Trail</div>', unsafe_allow_html=True)

    base = pd.read_csv(Path(__file__).parent / "docs" / "model_audit_log.csv")
    st.markdown("#### Responsible AI Records")
    st.dataframe(base, use_container_width=True, hide_index=True)

    if st.session_state.history:
        st.markdown("#### This Session")
        st.dataframe(
            pd.DataFrame(
                st.session_state.history,
                columns=["investigation_id","case_id","decision","commands"]
            ),
            use_container_width=True,
            hide_index=True
        )

    st.success("The included audit log contains five documented examples of human correction/override.")

# ---------- ARCHITECTURE ----------
else:
    st.markdown('<div class="section-title">ℹ️ NetSage AI Architecture</div>', unsafe_allow_html=True)

    layers = [
        ("01", "Case Data Layer", "30 structured Cisco Packet Tracer-style incidents."),
        ("02", "Deterministic Diagnostic Layer", "Python rules catch known Cisco configuration patterns."),
        ("03", "Evidence Intelligence", "Evidence scoring, contradiction detection and explainable evidence chain."),
        ("04", "AI Diagnostic Layer", "Gemini returns structured root cause, OSI layer, confidence, evidence, next command and fix steps."),
        ("05", "Command Safety", "Potentially disruptive CLI actions are risk-scored."),
        ("06", "Human Review Gate", "Accept / Edit + Accept / Reject."),
        ("07", "Audit Layer", "Investigation IDs and reviewer decisions make the workflow traceable.")
    ]

    for num, title, desc in layers:
        st.markdown(
            f'<div class="card" style="margin-bottom:10px;">'
            f'<span class="pill pill-purple">{num}</span>'
            f'<b style="font-size:1.05rem">{title}</b>'
            f'<div style="margin-top:6px;color:#aab5c7">{desc}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">⭐ Why this is more than a chatbot</div>', unsafe_allow_html=True)
    st.success(
        "Evidence-backed reasoning + deterministic verification + command-risk analysis + "
        "human approval + auditability in one Cisco troubleshooting workflow."
    )
