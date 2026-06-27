import streamlit as st
import tempfile, json, os
from pipeline.pdf_parser import extract_text
from pipeline.extractor import extract_codes
from pipeline.differ import compute_diff
from pipeline.llm_analyzer import analyze_diff

st.set_page_config(page_title="Policy Diff Tool", layout="wide")
st.title("Policy Change Highlighter")
st.caption("Upload two policy PDFs to detect and summarize what changed.")

col1, col2 = st.columns(2)
with col1:
    old_file = st.file_uploader("Old Policy (e.g. CY 2025)", type="pdf")
with col2:
    new_file = st.file_uploader("New Policy (e.g. CY 2026)", type="pdf")

if old_file and new_file and st.button("Run Analysis"):
    with st.spinner("Parsing PDFs..."):
        # Write uploads to temp files
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f1:
            f1.write(old_file.read()); old_path = f1.name
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f2:
            f2.write(new_file.read()); new_path = f2.name

        old_text = extract_text(old_path)
        new_text = extract_text(new_path)

    with st.spinner("Extracting codes..."):
        old_codes = extract_codes(old_text)
        new_codes = extract_codes(new_text)

    with st.spinner("Computing diff..."):
        diff = compute_diff(old_codes, new_codes)

    with st.spinner("Asking AI to analyze changes..."):
        analysis = analyze_diff(diff, old_text, new_text)

    # ── Results ──────────────────────────────────────────────
    
    # Status badge
    status = analysis.get("review_status", "unknown")
    color = {"auto_approved": "green", 
             "human_review_required": "orange", 
             "escalate_immediately": "red"}.get(status, "gray")
    st.markdown(f"### Status: :{color}[{status.replace('_', ' ').upper()}]")

    # Summary
    st.subheader("Summary")
    st.info(analysis.get("summary", ""))

    # Stats
    s = diff["stats"]
    m1, m2, m3 = st.columns(3)
    m1.metric("Codes Added", s["added_count"])
    m2.metric("Codes Deleted", s["deleted_count"])
    m3.metric("Codes Changed", s["changed_count"])

    # Classified changes table
    st.subheader("Classified Changes")
    changes = analysis.get("classified_changes", [])
    if changes:
        st.table(changes)

    # Ambiguities
    st.subheader("Ambiguities — Requires Human Review")
    for a in analysis.get("ambiguities", []):
        st.warning(f"**{a['text']}**\n\n{a['reason']}")

    # Analyst notes
    if analysis.get("analyst_notes"):
        st.subheader("Analyst Notes")
        st.write(analysis["analyst_notes"])

    # Raw JSON download
    st.download_button(
        "Download Full Report (JSON)",
        data=json.dumps({"diff": diff, "analysis": analysis}, indent=2),
        file_name="policy_diff_report.json",
        mime="application/json"
    )

    # Cleanup
    os.unlink(old_path); os.unlink(new_path)