import pandas as pd
import streamlit as st

from ui.adapters import ResumeLoadError, load_resume
from ui.components import (
    empty_state,
    note,
    page_header,
    section_label,
    section_status,
    skill_chips,
)
from ui.theme import setup_page

setup_page("Resume analysis")
page_header(
    "Resume analysis",
    "Upload a resume and check what was extracted before matching it to a job.",
)

NOTES = {
    "empty": "This file is empty, so there is nothing to analyse. Check that the right file was selected and try again.",
    "unsupported": "This file type is not supported. ResumeIQ reads PDF and DOCX files only.",
    "corrupted": "This file could not be opened. It may be damaged or password protected. Try exporting it again as a PDF or DOCX.",
    "text_poor": (
        "Very little selectable text was found in this file. If it is a scan or a photo of a resume, "
        "scanned images are not supported yet. Export a text-based PDF or upload a DOCX instead."
    ),
}


def _clear() -> None:
    st.session_state.pop("resume_analysis", None)
    st.session_state.pop("resume_file_id", None)


# ---- upload ----
uploaded = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")
st.markdown(
    '<div class="riq-caption">Files are processed locally and are not stored unless you choose to save.</div>',
    unsafe_allow_html=True,
)

if uploaded is not None:
    file_id = (uploaded.name, uploaded.size)
    if st.session_state.get("resume_file_id") != file_id:
        try:
            st.session_state["resume_analysis"] = load_resume(uploaded)
            st.session_state["resume_file_id"] = file_id
        except ResumeLoadError as err:
            _clear()
            note(NOTES.get(err.kind, NOTES["corrupted"]))
        except Exception:
            _clear()
            note(NOTES["corrupted"])

analysis = st.session_state.get("resume_analysis")

if analysis is None:
    if uploaded is None:
        st.write("")
        empty_state("No resume yet. Upload a PDF or DOCX to see the extracted text, sections and skills.")
    st.stop()

# ---- text and sections ----
st.write("")
left, right = st.columns([6, 4], gap="large")
with left:
    section_label("Extracted text")
    st.text_area(
        "Extracted text",
        value=analysis["text"],
        height=360,
        disabled=True,
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="riq-caption">Check this for parsing errors. Everything below is based on it.</div>',
        unsafe_allow_html=True,
    )
with right:
    section_label("Sections found")
    section_status(analysis["sections"])

# ---- skills by category ----
section_label("Skills by category")
for category, skills in analysis["skills_by_category"].items():
    c1, c2 = st.columns([2, 5], gap="large")
    c1.markdown(f"<div style='padding-top:4px'>{category}</div>", unsafe_allow_html=True)
    with c2:
        skill_chips(skills, "matched")

# ---- keywords ----
section_label("Keywords")
query = st.text_input("Search keywords", placeholder="Search by term, section or snippet")
df = pd.DataFrame(analysis["keywords"], columns=["term", "section", "snippet"])
df.columns = ["Term", "Section", "Snippet"]
if query.strip():
    q = query.strip().lower()
    mask = df.apply(lambda col: col.astype(str).str.lower().str.contains(q, regex=False)).any(axis=1)
    df = df[mask]
if df.empty:
    note("No keywords match that search.")
else:
    st.dataframe(df, hide_index=True, use_container_width=True)

# ---- continue ----
st.write("")
if st.button("Continue to job match", type="primary"):
    st.session_state["resume_analysis"] = analysis
    st.switch_page("pages/3_Job_Match.py")
