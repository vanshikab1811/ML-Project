"""Reusable UI components. Each emits plain HTML styled by ui/styles.css."""
from html import escape

import streamlit as st

MATCH_CAPTION = "Estimated resume-to-job alignment. Not a hiring prediction."

_CHIP_KINDS = {"matched", "missing", "extra"}


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def _html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def page_header(title: str, subtitle: str | None = None) -> None:
    sub = f'<p class="riq-subtitle">{escape(subtitle)}</p>' if subtitle else ""
    _html(f'<h1 class="riq-title">{escape(title)}</h1>{sub}')


def section_label(text: str) -> None:
    _html(f'<div class="riq-label">{escape(text)}</div>')


def score_display(value: float, caption: str = MATCH_CAPTION) -> None:
    """Large score with a thin bar. The caption defaults to the required disclaimer."""
    v = _clamp(value)
    _html(
        '<div class="riq-score">'
        f'<div><span class="riq-score-value">{v:.0f}</span><span class="riq-score-unit">/100</span></div>'
        f'<div class="riq-bar"><span style="width:{v:.1f}%"></span></div>'
        f'<div class="riq-caption">{escape(caption)}</div>'
        "</div>"
    )


def component_bars(components: dict) -> None:
    """One thin bar per component: label left, value right."""
    rows = []
    for key, value in components.items():
        v = _clamp(value)
        label = escape(str(key).replace("_", " ").capitalize())
        rows.append(
            '<div class="riq-comp">'
            f'<div class="riq-comp-row"><span>{label}</span><span>{v:.0f}</span></div>'
            f'<div class="riq-bar"><span style="width:{v:.1f}%"></span></div>'
            "</div>"
        )
    _html("".join(rows))


def skill_chips(skills, kind: str = "matched", soft: bool = False) -> None:
    """kind: 'matched' (teal), 'missing' (pink), 'extra' (neutral). soft lightens the fill to 50%."""
    if kind not in _CHIP_KINDS:
        raise ValueError(f"kind must be one of {sorted(_CHIP_KINDS)}")
    chips = "".join(f'<span class="riq-chip riq-chip-{kind}">{escape(str(s))}</span>' for s in skills)
    extra = " riq-chips-soft" if soft else ""
    _html(f'<div class="riq-chips{extra}">{chips}</div>')


def section_status(sections: dict) -> None:
    """List of resume sections: filled dot when present, hollow dot when missing."""
    rows = []
    for name, present in sections.items():
        dot = "riq-dot-on" if present else "riq-dot-off"
        state = "Present" if present else "Missing"
        rows.append(
            '<div class="riq-status">'
            f'<span class="riq-dot {dot}"></span><span>{escape(str(name).capitalize())}</span>'
            f'<span class="riq-status-state">{state}</span></div>'
        )
    _html("".join(rows))


def empty_state(message: str) -> None:
    _html(f'<div class="riq-empty">{escape(message)}</div>')


def note(text: str) -> None:
    _html(f'<div class="riq-note"><p>{escape(text)}</p></div>')

