"""Design system entry point: colour constants, CSS loader, Plotly template."""
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# Palette. Use only these (plus opacity of them).
BACKGROUND = "#F1F7F7"
PANEL = "#D5E5E5"
BORDER = "#BDD7D8"
NEUTRAL = "#DDD3D3"
ACCENT = "#F7CBCA"
TEXT = "#5D6B6B"

CSS_PATH = Path(__file__).parent / "styles.css"
TEMPLATE_NAME = "resumeiq"

_FONT = "DM Sans, sans-serif"


def _build_template() -> go.layout.Template:
    axis = dict(
        showline=False,
        zeroline=False,
        ticks="",
        tickfont=dict(family=_FONT, size=12, color=TEXT),
        title=dict(font=dict(family=_FONT, size=12, color=TEXT)),
    )
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=_FONT, size=13, color=TEXT),
        title=dict(text=""),
        colorway=[BORDER, NEUTRAL, TEXT, ACCENT],
        margin=dict(l=0, r=0, t=8, b=0),
        xaxis=dict(showgrid=False, **axis),
        yaxis=dict(showgrid=True, gridcolor=BORDER, gridwidth=1, **axis),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(family=_FONT, size=12, color=TEXT),
        ),
        hoverlabel=dict(bgcolor=BACKGROUND, bordercolor=BORDER, font=dict(family=_FONT, color=TEXT)),
        bargap=0.4,
    )
    template.data.bar = [go.Bar(marker=dict(color=BORDER, line=dict(width=0)))]
    return template


pio.templates[TEMPLATE_NAME] = _build_template()
pio.templates.default = TEMPLATE_NAME


def load_css() -> None:
    """Inject the global stylesheet into the current page."""
    css = CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def setup_page(title: str) -> None:
    """Call first in every page: page config, CSS and sidebar brand."""
    st.set_page_config(page_title=f"{title} | ResumeIQ", layout="wide", initial_sidebar_state="expanded")
    load_css()
    st.sidebar.markdown('<div class="riq-brand">ResumeIQ</div>', unsafe_allow_html=True)

