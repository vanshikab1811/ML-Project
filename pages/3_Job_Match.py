from html import escape

import plotly.graph_objects as go
import streamlit as st

from ui.adapters import DEFAULT_WEIGHTS, ResumeLoadError, analyse_job, load_job_file, score_match
from ui.components import (
    component_bars,
    empty_state,
    note,
    page_header,
    score_display,
    section_label,
    skill_chips,
)
from ui.theme import BORDER, NEUTRAL, TEMPLATE_NAME, setup_page

setup_page("Job match")
page_header("Job match", "Compare the resume with one job description.")

FILE_NOTES = {
    "empty": "This file is empty, so there is nothing to analyse.",
    "unsupported": "This file type is not supported. ResumeIQ reads PDF and DOCX files only.",
    "corrupted": "This file could not be opened. Try exporting it again as a PDF or DOCX.",
    "text_poor": "Very little selectable text was found. Scanned images are not supported yet.",
}


def chips_or_none(skills, kind, soft=False):
    if skills:
        skill_chips(skills, kind, soft=soft)
    else:
        st.markdown('<div class="riq-caption">None</div>', unsafe_allow_html=True)


resume = st.session_state.get("resume_analysis")
if resume is None:
    empty_state("No resume loaded. Upload one first, then come back to compare it with a job.")
    st.page_link("pages/2_Resume_Analysis.py", label="Go to Resume analysis")
    st.stop()

# ---- input ----
section_label("Job description")
tab_paste, tab_upload = st.tabs(["Paste text", "Upload file"])
with tab_paste:
    pasted = st.text_area(
        "Job description text",
        height=220,
        placeholder="Paste the full job description here",
        label_visibility="collapsed",
    )
with tab_upload:
    job_file = st.file_uploader("Job description file", type=["pdf", "docx"], label_visibility="collapsed")

if st.button("Analyse match", type="primary"):
    text, error = None, None
    if pasted.strip():
        text = pasted
    elif job_file is not None:
        try:
            text = load_job_file(job_file)
        except ResumeLoadError as err:
            error = FILE_NOTES.get(err.kind, FILE_NOTES["corrupted"])
    else:
        error = "Paste a job description or upload a file first."
    if error:
        note(error)
    elif text is not None:
        st.session_state["current_job"] = analyse_job(text)

job = st.session_state.get("current_job")
if job is None:
    st.stop()

# ---- weights ----
with st.expander("Adjust weights"):
    st.markdown(
        '<div class="riq-caption">For weight experiments. The three weights must sum to 1.</div>',
        unsafe_allow_html=True,
    )
    w_skill = st.slider("Skill", 0.0, 1.0, DEFAULT_WEIGHTS["skill"], 0.05, key="w_skill")
    w_text = st.slider("Text similarity", 0.0, 1.0, DEFAULT_WEIGHTS["text"], 0.05, key="w_text")
    w_exp = st.slider("Experience", 0.0, 1.0, DEFAULT_WEIGHTS["experience"], 0.05, key="w_exp")
    total = round(w_skill + w_text + w_exp, 2)
    valid = total == 1.0
    if not valid:
        st.markdown(
            f'<div class="riq-caption">Weights sum to {total:.2f}. Adjust them to 1.00 to apply; the defaults are in use.</div>',
            unsafe_allow_html=True,
        )

weights = {"skill": w_skill, "text": w_text, "experience": w_exp} if valid else dict(DEFAULT_WEIGHTS)
match = score_match(resume, job, weights=weights)

# ---- 1. top row ----
st.write("")
left, right = st.columns([1, 1], gap="large")
with left:
    st.markdown(f'<h2 class="riq-heading">{escape(job["title"])}</h2>', unsafe_allow_html=True)
    score_display(match["overall"])
with right:
    section_label("Score components")
    component_bars(match["components"])
    w = match["weights"]
    st.markdown(
        f'<div class="riq-caption">Weights used: skill {w["skill"]:.2f}, text {w["text"]:.2f}, experience {w["experience"]:.2f}.</div>',
        unsafe_allow_html=True,
    )

# ---- 2. explanation ----
section_label("Why this score")
note(match["explanation"])

# ---- 3. skills ----
st.write("")
c1, c2, c3 = st.columns(3, gap="large")
with c1:
    section_label("Matched")
    chips_or_none(match["matched"], "matched")
with c2:
    section_label("Missing required")
    chips_or_none(match["missing_required"], "missing")
with c3:
    section_label("Missing preferred")
    chips_or_none(match["missing_preferred"], "missing", soft=True)
section_label("Additional skills in your resume")
chips_or_none(match["extra"], "extra")

# ---- 4. chart ----
section_label("Skill coverage")
comp = match["components"]
fig = go.Figure(
    go.Bar(
        y=["Required", "Preferred"],
        x=[comp["required_skill_coverage"], comp["preferred_skill_coverage"]],
        orientation="h",
        marker=dict(color=[BORDER, NEUTRAL]),
        text=[f'{comp["required_skill_coverage"]:.0f}%', f'{comp["preferred_skill_coverage"]:.0f}%'],
        textposition="outside",
        cliponaxis=False,
        hoverinfo="skip",
    )
)
fig.update_layout(
    template=TEMPLATE_NAME,
    height=150,
    showlegend=False,
    xaxis=dict(range=[0, 100], ticksuffix="%", fixedrange=True),
    yaxis=dict(autorange="reversed", fixedrange=True),
    margin=dict(l=0, r=30, t=4, b=0),
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---- 5. caveats ----
note(
    "A missing keyword does not prove a missing skill; the resume may describe it in other words. "
    "Text similarity measures wording overlap, not competence."
)

# ---- 6. save ----
if st.button("Save this job for comparison"):
    jobs = st.session_state.setdefault("jobs", [])
    if any(j["title"] == job["title"] for j in jobs):
        st.markdown('<div class="riq-caption">This job is already saved.</div>', unsafe_allow_html=True)
    else:
        jobs.append(job)
        st.session_state.setdefault("match_results", {})[job["title"]] = match
        st.markdown('<div class="riq-caption">Saved. You can compare it on the Compare jobs page.</div>', unsafe_allow_html=True)
