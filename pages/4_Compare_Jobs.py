from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.adapters import analyse_job, score_match
from ui.components import empty_state, note, page_header, section_label, skill_chips
from ui.theme import ACCENT, BORDER, NEUTRAL, TEMPLATE_NAME, TEXT, setup_page

setup_page("Compare jobs")
page_header("Compare jobs", "Rank several job descriptions against the same resume.")

MIN_JOBS, MAX_JOBS = 2, 6

resume = st.session_state.get("resume_analysis")
if resume is None:
    empty_state("No resume loaded. Upload one first, then come back to compare it with several jobs.")
    st.page_link("pages/2_Resume_Analysis.py", label="Go to Resume analysis")
    st.stop()

# ---- job input slots ----
st.session_state.setdefault("cmp_slots", [0, 1])
st.session_state.setdefault("cmp_next_id", 2)
slots = st.session_state["cmp_slots"]
saved_jobs = st.session_state.get("jobs", [])


def add_slot():
    if len(st.session_state["cmp_slots"]) < MAX_JOBS:
        st.session_state["cmp_slots"].append(st.session_state["cmp_next_id"])
        st.session_state["cmp_next_id"] += 1


def remove_slot(slot_id):
    if len(st.session_state["cmp_slots"]) > MIN_JOBS:
        st.session_state["cmp_slots"].remove(slot_id)
        st.session_state.pop(f"cmp_label_{slot_id}", None)
        st.session_state.pop(f"cmp_text_{slot_id}", None)


section_label("Saved jobs")
saved_titles = [j["title"] for j in saved_jobs]
if saved_titles:
    chosen_saved = st.multiselect("Use saved jobs", saved_titles, placeholder="Choose from jobs saved on Job match")
else:
    chosen_saved = []
    st.markdown(
        '<div class="riq-caption">No saved jobs yet. Jobs saved on the Job match page appear here.</div>',
        unsafe_allow_html=True,
    )

section_label("Job descriptions")
for n, slot_id in enumerate(slots, start=1):
    with st.container(border=True):
        top, btn = st.columns([5, 1], vertical_alignment="bottom")
        top.text_input("Label", key=f"cmp_label_{slot_id}", placeholder=f"Job {n}")
        btn.button(
            "Remove",
            key=f"cmp_remove_{slot_id}",
            on_click=remove_slot,
            args=(slot_id,),
            disabled=len(slots) <= MIN_JOBS,
        )
        st.text_area(
            "Job description",
            key=f"cmp_text_{slot_id}",
            height=120,
            placeholder="Paste the job description",
            label_visibility="collapsed",
        )
st.button("Add another job", on_click=add_slot, disabled=len(slots) >= MAX_JOBS)
st.markdown(
    f'<div class="riq-caption">Between {MIN_JOBS} and {MAX_JOBS} jobs in total, including saved jobs.</div>',
    unsafe_allow_html=True,
)

st.write("")
if st.button("Compare jobs", type="primary"):
    entries = [(t, next(j for j in saved_jobs if j["title"] == t)) for t in chosen_saved]
    for n, slot_id in enumerate(slots, start=1):
        text = st.session_state.get(f"cmp_text_{slot_id}", "").strip()
        if text:
            label = st.session_state.get(f"cmp_label_{slot_id}", "").strip() or f"Job {n}"
            entries.append((label, analyse_job(text)))
    if len(entries) < MIN_JOBS:
        note("Add at least two jobs, by pasting descriptions or choosing saved jobs.")
    elif len(entries) > MAX_JOBS:
        note(f"Compare at most {MAX_JOBS} jobs at a time. Remove some and try again.")
    else:
        results, seen = [], {}
        for label, job in entries:
            seen[label] = seen.get(label, 0) + 1
            unique = label if seen[label] == 1 else f"{label} ({seen[label]})"
            results.append({"label": unique, "job": job, "match": score_match(resume, job)})
        st.session_state["compare_results"] = results

results = st.session_state.get("compare_results")
if not results:
    st.stop()

# ---- 1. ranking ----
section_label("Ranking")
order = sorted(range(len(results)), key=lambda i: -results[i]["match"]["overall"])
rank_of = {i: r for r, i in enumerate(order, start=1)}
rows = []
for i, r in enumerate(results):
    m = r["match"]
    c = m["components"]
    rows.append(
        {
            "Rank": rank_of[i],
            "Job": r["label"],
            "Overall": m["overall"],
            "Required coverage": c["required_skill_coverage"],
            "Preferred coverage": c["preferred_skill_coverage"],
            "Text similarity": c["text_similarity"],
            "Missing required": len(m["missing_required"]),
        }
    )
df = pd.DataFrame(rows)

f1, f2 = st.columns(2, gap="large")
sort_by = f1.selectbox("Sort by", list(df.columns), index=0)
min_score = f2.slider("Minimum overall score", 0, 100, 0)

ascending = sort_by in ("Rank", "Job", "Missing required")
view = df[df["Overall"] >= min_score].sort_values(sort_by, ascending=ascending, kind="stable")
if view.empty:
    note("No jobs are at or above that score. Lower the minimum to see them.")
else:
    st.dataframe(
        view,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Overall": st.column_config.NumberColumn(format="%.0f"),
            "Required coverage": st.column_config.NumberColumn(format="%.0f"),
            "Preferred coverage": st.column_config.NumberColumn(format="%.0f"),
            "Text similarity": st.column_config.NumberColumn(format="%.0f"),
        },
    )
st.markdown(
    f'<div class="riq-caption">Showing {len(view)} of {len(df)} jobs. '
    f'Sorted by {escape(sort_by.lower())}, {"ascending" if ascending else "descending"}. '
    "Scores are estimated resume-to-job alignment, not hiring predictions.</div>",
    unsafe_allow_html=True,
)

# ---- 2. score breakdown ----
section_label("Score breakdown")
COMPONENTS = [
    ("required_skill_coverage", "Required skills", BORDER),
    ("preferred_skill_coverage", "Preferred skills", NEUTRAL),
    ("text_similarity", "Text similarity", TEXT),
    ("keyword_coverage", "Keywords", "rgba(93, 107, 107, 0.55)"),
    ("experience_relevance", "Experience", "rgba(93, 107, 107, 0.25)"),
]
labels = [results[i]["label"] for i in order]
fig = go.Figure()
for key, name, colour in COMPONENTS:
    fig.add_bar(
        y=labels,
        x=[results[i]["match"]["components"][key] for i in order],
        name=name,
        orientation="h",
        marker=dict(color=colour),
        hovertemplate="%{y}: %{x:.0f}<extra>" + name + "</extra>",
    )
fig.update_layout(
    template=TEMPLATE_NAME,
    barmode="group",
    bargap=0.3,
    bargroupgap=0.05,
    height=120 + 120 * len(labels),
    xaxis=dict(range=[0, 100], fixedrange=True),
    yaxis=dict(autorange="reversed", fixedrange=True),
    legend=dict(traceorder="normal"),
    margin=dict(l=0, r=0, t=30, b=0),
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---- 3. skills across jobs ----
section_label("Skills asked for across these jobs")
resume_skills = {s.lower() for skills in resume["skills_by_category"].values() for s in skills}
for r in results:
    resume_skills |= {s.lower() for s in r["match"]["matched"]}
counts = {}
for r in results:
    for s in dict.fromkeys(r["job"]["required_skills"] + r["job"]["preferred_skills"]):
        counts[s] = counts.get(s, 0) + 1
top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
skill_names = [s for s, _ in top]
fig2 = go.Figure(
    go.Bar(
        y=skill_names,
        x=[c for _, c in top],
        orientation="h",
        marker=dict(color=[BORDER if s.lower() in resume_skills else ACCENT for s in skill_names]),
        text=[c for _, c in top],
        textposition="outside",
        cliponaxis=False,
        hoverinfo="skip",
    )
)
fig2.update_layout(
    template=TEMPLATE_NAME,
    showlegend=False,
    height=60 + 32 * len(skill_names),
    xaxis=dict(dtick=1, range=[0, len(results) + 0.5], fixedrange=True, showticklabels=False),
    yaxis=dict(autorange="reversed", fixedrange=True),
    margin=dict(l=0, r=20, t=4, b=0),
)
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
st.markdown(
    f'<div class="riq-caption">Number of jobs, out of {len(results)}, that ask for each skill. '
    "Teal bars are skills your resume has; pink bars are missing.</div>",
    unsafe_allow_html=True,
)

# ---- 4. compare two jobs ----
section_label("Compare two jobs")
names = [r["label"] for r in results]
s1, s2 = st.columns(2, gap="large")
pick_a = s1.selectbox("First job", names, index=0, key="cmp_pick_a")
pick_b = s2.selectbox("Second job", names, index=min(1, len(names) - 1), key="cmp_pick_b")
by_label = {r["label"]: r for r in results}
col_a, col_b = st.columns(2, gap="large")
for col, pick in ((col_a, pick_a), (col_b, pick_b)):
    m = by_label[pick]["match"]
    with col:
        st.markdown(
            f'<div class="riq-comp-row"><span>{escape(pick)}</span><span>{m["overall"]:.0f}</span></div>',
            unsafe_allow_html=True,
        )
        section_label("Matched")
        skill_chips(m["matched"], "matched") if m["matched"] else st.markdown(
            '<div class="riq-caption">None</div>', unsafe_allow_html=True
        )
        section_label("Missing")
        if m["missing_required"] or m["missing_preferred"]:
            if m["missing_required"]:
                skill_chips(m["missing_required"], "missing")
            if m["missing_preferred"]:
                skill_chips(m["missing_preferred"], "missing", soft=True)
        else:
            st.markdown('<div class="riq-caption">None</div>', unsafe_allow_html=True)

# ---- 5. caveat ----
st.write("")
note("Scores are estimates of document alignment, not hiring predictions.")
