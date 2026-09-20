"""Shared visual theme and layout helpers for every Streamlit page.

Centralizing this avoids repeating the same CSS block and header markup
on every page. Uses Streamlit's supported `st.container(key=...)` hook
(which renders as a `.st-key-<key>` CSS class) instead of undocumented
internal class names, so the styling does not break on Streamlit upgrades.
"""

import streamlit as st

ACCENT = "#6366F1"
FOREGROUND = "#252B31"
MUTED = "#8A9496"
BORDER = "#E5E5E5"

CHART_PALETTE = {
    "primary": FOREGROUND,
    "accent": ACCENT,
    "positive": "#3E8E5A",
    "negative": "#C2483D",
}


def apply_theme() -> None:
    """Inject fonts and CSS shared by every page. Call this first on each page."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}
        h1, h2, h3 {{
            font-family: 'Instrument Serif', serif;
            letter-spacing: -0.01em;
        }}
        [data-testid="stMetricValue"] {{
            font-family: 'Instrument Serif', serif;
            font-size: 2rem;
        }}
        [data-testid="stMetricLabel"] {{
            color: {MUTED};
            font-size: 0.8rem;
        }}
        .stButton > button, .stDownloadButton > button {{
            border-radius: 999px;
            font-weight: 500;
        }}
        [data-testid="stSidebarNav"] li div a {{
            font-size: 0.9rem;
        }}
        .st-key-hero_badge {{
            display: inline-block;
            border: 1px solid {BORDER};
            border-radius: 999px;
            padding: 0.3rem 1rem;
            font-size: 0.8rem;
            color: {MUTED};
            margin-bottom: 0.5rem;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 1rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "") -> None:
    """Consistent big-serif title + muted subtitle, used at the top of every page."""
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f":gray[{subtitle}]")


def how_it_works() -> None:
    """Five-step wayfinding stepper explaining the app's flow, shown on the home page."""
    steps = [
        ("1", "Financials", "Read the historical numbers (2021-2025)."),
        ("2", "Forecast", "Set Revenue Growth & EBITDA Margin for 2026-2028."),
        ("3", "Valuation", "Turn that forecast into an Enterprise / Equity Value (DCF)."),
        ("4", "Sensitivity", "See how much WACC, growth & margin move that value."),
        ("5", "Scenarios", "Compare Downside / Base / Upside side by side."),
    ]
    cols = st.columns(len(steps))
    for col, (number, label, description) in zip(cols, steps):
        with col:
            with st.container(border=True):
                st.markdown(
                    f"<span style='color:{ACCENT}; font-family:\"Instrument Serif\", serif; "
                    f"font-size:1.5rem;'>{number}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"**{label}**")
                st.caption(description)
