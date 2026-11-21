from html import escape

import streamlit as st

from ui.components import (
    component_bars,
    empty_state,
    history_toggle,
    note,
    page_header,
    score_display,
    section_label,
    skill_chips,
)
from ui.history_store import delete_all, delete_analysis, list_analyses
from ui.theme import setup_page

setup_page("History")
page_header("History", "Saved analyses and how they change after a resume update.")

history_toggle()
note(
    "When saving is on, ResumeIQ stores only the job title, date, scores and skill lists of each analysis in "
    "database/resumeiq.db, never the resume text or contact details. Delete a record or all history below, "
    "or delete that file to remove everything."
)

history = list_analyses()
if not history:
    st.write("")
    empty_state("No saved analyses. Turn on saving, then run a job match, and it will be listed here.")
    st.page_link("pages/3_Job_Match.py", label="Go to Job match")
    st.stop()

# ---- table ----
section_label("Saved analyses")
widths = [2.2, 3.5, 1.2, 1.1, 1.1]
head = st.columns(widths)
for col, text in zip(head, ["Date", "Job", "Score", "", ""]):
    col.markdown(f'<div class="riq-caption">{text}</div>', unsafe_allow_html=True)
for a in history:
    c = st.columns(widths, vertical_alignment="center")
    c[0].markdown(escape(a["created_at"]))
    c[1].markdown(escape(a["job_title"]))
    c[2].markdown(f'{a["overall"]:.0f}')
    if c[3].button("View", key=f"view_{a['id']}"):
        st.session_state["history_view"] = a["id"]
    if c[4].button("Delete", key=f"delete_{a['id']}"):
        delete_analysis(a["id"])
        if st.session_state.get("history_view") == a["id"]:
            st.session_state.pop("history_view", None)
        st.rerun()

st.markdown(
    '<div class="riq-caption" style="margin-top:8px">Scores are estimated resume-to-job alignment, not hiring predictions.</div>',
    unsafe_allow_html=True,
)

# ---- delete all with confirmation ----
st.write("")
if st.session_state.get("confirm_delete_all"):
    note("This permanently removes every saved analysis. It cannot be undone.")
    d1, d2, _ = st.columns([1.4, 1, 3])
    if d1.button("Yes, delete all", type="primary"):
        delete_all()
        st.session_state.pop("history_view", None)
        st.session_state["confirm_delete_all"] = False
        st.rerun()
    if d2.button("Cancel"):
        st.session_state["confirm_delete_all"] = False
        st.rerun()
else:
    if st.button("Delete all history"):
        st.session_state["confirm_delete_all"] = True
        st.rerun()

# ---- view one ----
view_id = st.session_state.get("history_view")
selected = next((a for a in history if a["id"] == view_id), None)
if selected:
    section_label("Saved analysis")
    st.markdown(f'<h2 class="riq-heading">{escape(selected["job_title"])}</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="riq-caption">{escape(selected["created_at"])}</div>', unsafe_allow_html=True)
    v1, v2 = st.columns(2, gap="large")
    with v1:
        score_display(selected["overall"])
    with v2:
        component_bars(selected["scores"])
    s = selected["skills"]
    k1, k2, k3 = st.columns(3, gap="large")
    for col, label, key, kind, soft in (
        (k1, "Matched", "matched", "matched", False),
        (k2, "Missing required", "missing_required", "missing", False),
        (k3, "Missing preferred", "missing_preferred", "missing", True),
    ):
        with col:
            section_label(label)
            if s[key]:
                skill_chips(s[key], kind, soft=soft)
            else:
                st.markdown('<div class="riq-caption">None</div>', unsafe_allow_html=True)

# ---- compare with previous ----
section_label("Compare with previous")
titles = sorted({a["job_title"] for a in history if sum(b["job_title"] == a["job_title"] for b in history) >= 2})
if not titles:
    st.markdown(
        '<div class="riq-caption">Save two analyses of the same job, for example before and after a resume update, to compare them.</div>',
        unsafe_allow_html=True,
    )
else:
    title = st.selectbox("Job", titles)
    same = [a for a in history if a["job_title"] == title]  # newest first
    labels = {a["id"]: f'{a["created_at"]} (score {a["overall"]:.0f})' for a in same}
    p1, p2 = st.columns(2, gap="large")
    earlier_id = p1.selectbox("Earlier", [a["id"] for a in same], index=1, format_func=labels.get, key="cmp_earlier")
    later_id = p2.selectbox("Later", [a["id"] for a in same], index=0, format_func=labels.get, key="cmp_later")
    earlier = next(a for a in same if a["id"] == earlier_id)
    later = next(a for a in same if a["id"] == later_id)

    col_a, col_b = st.columns(2, gap="large")
    for col, a in ((col_a, earlier), (col_b, later)):
        with col:
            st.markdown(f'<div class="riq-caption">{escape(a["created_at"])}</div>', unsafe_allow_html=True)
            score_display(a["overall"])
            component_bars(a["scores"])
    delta = later["overall"] - earlier["overall"]
    direction = "up" if delta > 0 else "down" if delta < 0 else "unchanged"
    summary = (
        f"Score is {direction} by {abs(delta):.1f} points."
        if delta
        else "Score is unchanged between these two analyses."
    )
    st.markdown(f"<p>{summary}</p>", unsafe_allow_html=True)
    gained = [x for x in later["skills"]["matched"] if x not in earlier["skills"]["matched"]]
    section_label("Newly matched since the earlier analysis")
    if gained:
        skill_chips(gained, "matched")
    else:
        st.markdown('<div class="riq-caption">None</div>', unsafe_allow_html=True)
