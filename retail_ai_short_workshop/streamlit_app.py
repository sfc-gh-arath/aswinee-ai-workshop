from pathlib import Path

import streamlit as st

from components import is_session_complete

_DIR = Path(__file__).parent


def _title(session_num: int, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_session_complete(session_num) else ""
    return f"{session_num}. {label}{check}"


st.set_page_config(
    page_title="Retail AI Workshop (90 min)",
    page_icon=":material/storefront:",
    layout="wide",
)

st.logo(
    str(_DIR / "static" / "snowflake_full_logo.png"),
    icon_image=str(_DIR / "static" / "snowflake_logo.png"),
)

page = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
            st.Page("app_pages/getting_started.py", title="Getting Started", icon=":material/rocket_launch:"),
            st.Page("app_pages/agenda.py", title="Agenda", icon=":material/calendar_today:"),
        ],
        "Setup": [
            st.Page("app_pages/session_01.py", title=_title(1, "Foundation & Reference Data"), icon=":material/architecture:"),
            st.Page("app_pages/session_02.py", title=_title(2, "Data Prep & Features"), icon=":material/database:"),
        ],
        "AI Features": [
            st.Page("app_pages/session_03.py", title=_title(3, "Cortex LLM Functions"), icon=":material/psychology:"),
            st.Page("app_pages/session_04.py", title=_title(4, "Cortex Search & RAG"), icon=":material/search:"),
            st.Page("app_pages/session_05.py", title=_title(5, "Semantic Views & Analyst"), icon=":material/chat:"),
            st.Page("app_pages/session_06.py", title=_title(6, "Cortex Agents"), icon=":material/smart_toy:"),
        ],
        "Wrap-up": [
            st.Page("app_pages/session_07.py", title=_title(7, "Free-form Exploration"), icon=":material/explore:"),
        ],
    },
    position="sidebar",
)

page.run()
