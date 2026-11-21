from html import escape

import streamlit as st

from ui.adapters import get_recommendations, skill_category
from ui.components import empty_state, note, page_header, section_label
from ui.theme import setup_page

setup_page("Learning roadmap")
page_header("Skill gaps and learning roadmap", "Prioritised skill gaps with learning actions and projects.")

PRIORITIES = ["high", "medium", "low"]

results = st.session_state.get("match_results") or {}
if not results:
    empty_state(
        "No skill gaps to show yet. Analyse a job on Job match and save it, and the gaps will be listed here."
    )
    st.page_link("pages/3_Job_Match.py", label="Go to Job match")
    st.stop()

jobs = st.session_state.get("jobs", [])
missing = []
for m in results.values():
    missing += m["missing_required"] + m["missing_preferred"]
missing = list(dict.fromkeys(missing))

if not missing:
    empty_state("No gaps found. Every required and preferred skill in your saved jobs appears in the resume.")
    st.stop()

recs = get_recommendations(missing, jobs)
for r in recs:
    r["_category"] = skill_category(r["skill"])

# ---- filters ----
f1, f2 = st.columns(2, gap="large")
pick_priority = f1.selectbox("Priority", ["All", "High", "Medium", "Low"])
pick_category = f2.selectbox("Category", ["All"] + sorted({r["_category"] for r in recs}))

visible = [
    r
    for r in recs
    if (pick_priority == "All" or r["priority"] == pick_priority.lower())
    and (pick_category == "All" or r["_category"] == pick_category)
]


def safe_url(url: str) -> str:
    return url if url.startswith(("http://", "https://")) else ""


# ---- grouped blocks ----
if not visible:
    st.write("")
    note("No recommendations match these filters.")
for priority in PRIORITIES:
    group = sorted((r for r in visible if r["priority"] == priority), key=lambda r: r["skill"])
    if not group:
        continue
    section_label(f"{priority.capitalize()} priority")
    for r in group:
        with st.container(border=True):
            st.markdown(
                '<div class="riq-skill-head">'
                f'<span class="riq-skill-name">{escape(r["skill"])}</span>'
                f'<span class="riq-tag riq-tag-{priority}">{priority.capitalize()}</span>'
                f'<span class="riq-skill-cat">{escape(r["_category"])}</span></div>'
                f'<p class="riq-reason">{escape(r["reason"])}</p>',
                unsafe_allow_html=True,
            )
            learn, build = st.columns(2, gap="large")
            url = safe_url(r["resource_url"])
            link = (
                f'<p><a href="{escape(url)}" target="_blank" rel="noopener noreferrer">Open resource</a></p>'
                if url
                else ""
            )
            with learn:
                st.markdown(
                    f'<div class="riq-label" style="margin-top:0.5rem">Learn</div><p>{escape(r["learning_action"])}</p>{link}',
                    unsafe_allow_html=True,
                )
            with build:
                st.markdown(
                    f'<div class="riq-label" style="margin-top:0.5rem">Build</div><p>{escape(r["project_name"])}</p>',
                    unsafe_allow_html=True,
                )

# ---- how priority is decided ----
st.write("")
note(
    "Priority is set by simple rules. Skills a job lists as required rank above preferred ones, skills that "
    "appear in more of your saved jobs rank higher, and skills closer to the target roles rank above "
    "unrelated ones. Suggestions come from a curated list of learning actions and projects. They are "
    "rule-based, not the output of a learned recommender, and a missing keyword does not prove a missing skill."
)

# ---- export ----
lines = ["ResumeIQ learning roadmap", "Rule-based suggestions from a curated list. Not a hiring prediction.", ""]
for priority in PRIORITIES:
    for r in sorted((x for x in recs if x["priority"] == priority), key=lambda x: x["skill"]):
        lines += [
            f'{r["skill"]} ({priority} priority, {r["_category"]})',
            f'  Why: {r["reason"]}',
            f'  Learn: {r["learning_action"]}',
            f'  Resource: {r["resource_url"]}',
            f'  Build: {r["project_name"]}',
            "",
        ]
st.download_button(
    "Download roadmap as text",
    data="\n".join(lines),
    file_name="resumeiq_roadmap.txt",
    mime="text/plain",
)
