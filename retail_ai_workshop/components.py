import streamlit as st

SESSION_PROMPTS = {
    1: ["Prompt 1.1", "Prompt 1.2"],
    2: ["Prompt 2.1", "Prompt 2.2", "Prompt 2.3", "Prompt 2.4"],
    3: ["Prompt 3.1", "Prompt 3.2", "Prompt 3.3"],
    4: ["Prompt 4.1", "Prompt 4.2", "Prompt 4.3", "Prompt 4.4", "Prompt 4.5"],
    5: ["Prompt 5.1", "Prompt 5.2"],
    6: ["Prompt 6.1", "Prompt 6.2", "Prompt 6.3"],
    7: ["Prompt 7.1", "Prompt 7.2", "Prompt 7.3"],
    8: ["Prompt 8.1", "Prompt 8.2", "Prompt 8.3"],
    9: ["Prompt 9.1", "Prompt 9.2"],
    10: ["Prompt 10.1", "Prompt 10.2", "Prompt 10.3", "Prompt 10.4"],
    11: ["Prompt 11.1", "Prompt 11.2", "Prompt 11.3", "Prompt 11.4"],
    12: ["Prompt 12.1", "Prompt 12.2", "Prompt 12.3", "Prompt 12.4"],
    13: ["Prompt 13.1", "Prompt 13.2", "Prompt 13.3"],
}


def _done_store() -> dict:
    if "_done" not in st.session_state:
        st.session_state["_done"] = {}
    return st.session_state["_done"]


def _prompt_key(prompt_id: str) -> str:
    return prompt_id.replace(" ", "_").replace(".", "_")


def _on_toggle(prompt_id: str):
    key = _prompt_key(prompt_id)
    _done_store()[key] = st.session_state[f"_cb_{key}"]


def is_session_complete(session_num: int) -> bool:
    prompts = SESSION_PROMPTS.get(session_num, [])
    store = _done_store()
    return len(prompts) > 0 and all(
        store.get(_prompt_key(p), False) for p in prompts
    )


def render_prompt(prompt_id: str, title: str, prompt_text: str):
    key = _prompt_key(prompt_id)
    cb_key = f"_cb_{key}"
    store = _done_store()
    if cb_key not in st.session_state:
        st.session_state[cb_key] = store.get(key, False)
    with st.container(border=True):
        header_col, check_col = st.columns([5, 1])
        with header_col:
            st.markdown(f"#### :material/terminal: {prompt_id} - {title}")
        with check_col:
            st.checkbox(
                "Done",
                key=cb_key,
                on_change=_on_toggle,
                args=(prompt_id,),
            )
        st.caption("Copy this prompt and paste it into Cortex Code")
        st.code(prompt_text, language="text", wrap_lines=True)


def render_fallback_sql(title: str, sql_text: str, language: str = "sql"):
    label = "SQL" if language == "sql" else "code"
    with st.expander(f":material/bolt: Optional: Fallback {label} instead of the prompt — {title}", expanded=False):
        if language == "sql":
            st.caption("Short on time? Paste this into a Snowsight SQL worksheet and choose Run All instead of using the prompt above.")
        elif language == "python":
            st.caption("Short on time? Paste this into a cell of a Snowflake Notebook and run it instead of using the prompt above.")
        else:
            st.caption("Short on time? Run these commands in a terminal instead of using the prompt above.")
        st.code(sql_text, language=language, wrap_lines=True)


def render_explanation(title: str, body: str):
    with st.expander(f":material/school: {title}", expanded=False):
        st.markdown(body)


def render_technology_card(name: str, description: str, icon: str = "widgets"):
    with st.container(border=True):
        st.markdown(f":material/{icon}: **{name}**")
        st.caption(description)


def render_technologies_used(technologies: list[dict]):
    st.markdown("##### :material/build: Technologies used in this session")
    cols = st.columns(min(len(technologies), 3))
    for i, tech in enumerate(technologies):
        with cols[i % len(cols)]:
            render_technology_card(
                tech["name"], tech["description"], tech.get("icon", "widgets")
            )


def render_session_header(
    session_num: int,
    title: str,
    time_range: str,
    duration: str,
    building: str,
):
    st.title(f"Session {session_num}: {title}")
    col1, col2 = st.columns(2)
    col1.markdown(f":material/schedule: **{time_range}** ({duration})")
    col2.markdown(f":material/construction: **Building**: {building}")
    st.space("small")


def render_key_concepts(concepts: list[dict]):
    st.markdown("##### :material/lightbulb: Key concepts")
    for concept in concepts:
        with st.expander(f"**{concept['term']}**"):
            st.markdown(concept["definition"])


def render_domain_glossary(terms: list[dict]):
    st.markdown("##### :material/menu_book: Domain glossary")
    st.caption("Terms specific to the retail apparel and footwear industry")
    for term in terms:
        with st.expander(f"**{term['term']}**"):
            st.markdown(term["definition"])


def render_what_you_will_build(items: list[str]):
    st.markdown("##### :material/flag: What you will build in this session")
    for item in items:
        st.markdown(f"- :blue-badge[Goal] {item}")
    st.space("small")


def render_pro_tip(title: str, body: str):
    st.markdown(f"##### :material/star: Pro Tip: {title}")
    with st.container(border=True):
        st.markdown(body)


def render_what_you_built(items: list[str]):
    st.markdown("##### :material/check_circle: What you built in this session")
    for item in items:
        st.markdown(f"- :green-badge[Done] {item}")
