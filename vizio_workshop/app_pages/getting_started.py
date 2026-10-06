import streamlit as st

st.title("Getting Started")
st.markdown("Set up your Snowflake environment for the lab")

st.space("small")

st.markdown("#### Step 1: Access your Snowflake account")
with st.container(border=True):
    st.markdown("""
Log in to Snowsight using the credentials provided by your workshop facilitator.

| Setting | Value |
|---------|-------|
| **Account URL** | Provided at the start of the lab |
| **Username** | Your assigned username |
| **Role** | ACCOUNTADMIN |
""")

st.space("small")

st.markdown("#### Step 2: Open Cortex Code")
with st.container(border=True):
    st.markdown("""
Once logged in to Snowsight, open **Cortex Code (CoCo)** from the **right side** of the navigation bar.
Look for the **blue sparkle icon** (✦) in the top-right corner of Snowsight — click it to open or move the CoCo panel.

> :material/info: The icon looks like a **blue square with a white sparkle (✦)** and has the tooltip **"Open or move CoCo"**.

Confirm you are using the **ACCOUNTADMIN** role — you can check and switch roles in the bottom-left of the Snowsight UI.
""")

st.space("small")

st.markdown("#### Step 3: Enable cross-region inference")
with st.container(border=True):
    st.markdown("""
Several sessions use Cortex LLM models that require cross-region inference. Enable it:

```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```
""")

st.space("small")

st.markdown("#### Step 4: Verify Cortex Code is working")
with st.container(border=True):
    st.markdown("""
Test by pasting this prompt:

```
Show me the current role, warehouse, and database I'm using
```
""")

st.space("small")

st.markdown("#### Lab environment details")
col1, col2, col3 = st.columns(3)
col1.metric("Duration", "2 hours", help="Total lab time")
col2.metric("Compute", "Pre-provisioned", help="Warehouse configured in Session 1")
col3.metric("Support", "Facilitators on-site", help="Raise your hand if stuck")
