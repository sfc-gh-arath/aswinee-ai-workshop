from pathlib import Path

import streamlit as st

from components import is_session_complete

_DIR = Path(__file__).parent


def _title(session_num: int, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_session_complete(session_num) else ""
    return f"{session_num}. {label}{check}"


st.set_page_config(
    page_title="Store Inventory Optimization Lab",
    page_icon=":material/inventory_2:",
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
        "Data Foundation": [
            st.Page("app_pages/session_01.py", title=_title(1, "Foundation & Data Setup"), icon=":material/architecture:"),
            st.Page("app_pages/session_02.py", title=_title(2, "Data Discovery"), icon=":material/search:"),
        ],
        "Analytics Layer": [
            st.Page("app_pages/session_03.py", title=_title(3, "Analytics-Ready Views"), icon=":material/view_quilt:"),
            st.Page("app_pages/session_04.py", title=_title(4, "Dynamic Tables"), icon=":material/autorenew:"),
        ],
        "Applications": [
            st.Page("app_pages/session_05.py", title=_title(5, "Streamlit What-If App"), icon=":material/dashboard:"),
        ],
        "AI & Conversational BI": [
            st.Page("app_pages/session_06.py", title=_title(6, "Semantic View & Analyst"), icon=":material/chat:"),
            st.Page("app_pages/session_07.py", title=_title(7, "Cortex Search"), icon=":material/manage_search:"),
            st.Page("app_pages/session_08.py", title=_title(8, "Cortex Agent & CoWork"), icon=":material/smart_toy:"),
        ],
        "Wrap-up": [
            st.Page("app_pages/session_09.py", title="9. Try It Yourself", icon=":material/explore:"),
        ],
    },
    position="sidebar",
)

page.run()
