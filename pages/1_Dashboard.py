from html import escape

import plotly.graph_objects as go
import streamlit as st

from ui.adapters import skill_category
from ui.components import MATCH_CAPTION, empty_state, page_header, section_label, stat_row
from ui.history_store import list_analyses
from ui.theme import ACCENT, BORDER, TEMPLATE_NAME, setup_page

setup_page("Dashboard")
page_header("Dashboard", "Saved resume-to-job analyses, common skill gaps and the skills you have.")

history = list_analyses()
if not history:
    empty_state(
        "No saved analyses yet. Analyse your resume against a job, with saving turned on, and the summary will appear here."
    )
    st.page_link("pages/2_Resume_Analysis.py", label="Go to Resume analysis")
    st.page_link("pages/6_History.py", label="Turn on saving in History")
    st.stop()

# ---- numbers ----
gaps = {}
for a in history:
    for s in a["skills"]["missing_required"] + a["skills"]["missing_preferred"]:
        gaps[s] = gaps.get(s, 0) + 1
top_gap = max(gaps.items(), key=lambda kv: (kv[1], kv[0]))[0] if gaps else "None"
average = sum(a["overall"] for a in history) / len(history)

st.write("")
stat_row(
    [
        (str(len(history)), "analyses run"),
        (str(len({a["job_title"] for a in history})), "jobs analysed"),
        (f"{average:.0f}", "average estimated match (descriptive only)"),
        (top_gap, "most common gap"),
    ]
)
st.markdown(f'<div class="riq-caption">Scores are out of 100. {MATCH_CAPTION}</div>', unsafe_allow_html=True)

# ---- charts ----
left, right = st.columns(2, gap="large")
with left:
    section_label("Most common skill gaps")
    if gaps:
        top = sorted(gaps.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
        fig = go.Figure(
            go.Bar(
                y=[s for s, _ in top],
                x=[c for _, c in top],
                orientation="h",
                marker=dict(color=ACCENT),
                text=[c for _, c in top],
                textposition="outside",
                cliponaxis=False,
                hoverinfo="skip",
            )
        )
        fig.update_layout(
            template=TEMPLATE_NAME,
            height=60 + 32 * len(top),
            xaxis=dict(showticklabels=False, fixedrange=True, range=[0, max(c for _, c in top) + 1]),
            yaxis=dict(autorange="reversed", fixedrange=True),
            margin=dict(l=0, r=20, t=4, b=0),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            '<div class="riq-caption">Number of saved analyses in which each skill was missing.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="riq-caption">No gaps in the saved analyses.</div>', unsafe_allow_html=True)

with right:
    section_label("Skills distribution by category")
    seen = set()
    for a in history:
        seen |= set(a["skills"]["matched"]) | set(a["skills"]["extra"])
    by_category = {}
    for s in seen:
        c = skill_category(s)
        by_category[c] = by_category.get(c, 0) + 1
    if by_category:
        cats = sorted(by_category.items(), key=lambda kv: (-kv[1], kv[0]))
        fig2 = go.Figure(
            go.Bar(
                y=[c for c, _ in cats],
                x=[n for _, n in cats],
                orientation="h",
                marker=dict(color=BORDER),
                text=[n for _, n in cats],
                textposition="outside",
                cliponaxis=False,
                hoverinfo="skip",
            )
        )
        fig2.update_layout(
            template=TEMPLATE_NAME,
            height=60 + 32 * len(cats),
            xaxis=dict(showticklabels=False, fixedrange=True, range=[0, max(n for _, n in cats) + 1]),
            yaxis=dict(autorange="reversed", fixedrange=True),
            margin=dict(l=0, r=20, t=4, b=0),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            '<div class="riq-caption">Distinct resume skills seen across saved analyses.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="riq-caption">No skills in the saved analyses.</div>', unsafe_allow_html=True)

# ---- recent ----
section_label("Recent analyses")
rows = "".join(
    '<div class="riq-row">'
    f'<span>{escape(a["job_title"])}</span>'
    f'<span class="riq-row-meta">{escape(a["created_at"])}</span>'
    f'<span class="riq-row-score">{a["overall"]:.0f}</span></div>'
    for a in history[:5]
)
st.markdown(rows, unsafe_allow_html=True)
st.markdown(f'<div class="riq-caption" style="margin-top:8px">Scores are out of 100. {MATCH_CAPTION}</div>', unsafe_allow_html=True)
