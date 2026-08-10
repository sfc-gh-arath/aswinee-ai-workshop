import streamlit as st

st.title("Getting Started")
st.markdown("Set up your Snowflake environment for the lab")

st.space("small")

st.markdown("#### Step 1: Access your Snowflake account")

with st.container(border=True):
    st.markdown("""
Your lab environment has been pre-provisioned. Log in to Snowsight using the credentials
provided by your workshop facilitator.

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
Once logged in to Snowsight, open **Cortex Code** from the left navigation panel.
This is the AI coding assistant where you will paste all prompts from this workshop.

Confirm you are using the **ACCOUNTADMIN** role — you can check and switch roles in the
bottom-left of the Snowsight UI.
""")

st.space("small")

st.markdown("#### Step 3: Enable cross-region inference")

with st.container(border=True):
    st.markdown("""
Several sessions use Cortex LLM models that require cross-region inference. Enable it by
running this SQL in a worksheet (or ask Cortex Code to do it):

```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

This allows Snowflake to route LLM requests to the nearest available region if the model
is not hosted in your account's home region.
""")

st.space("small")

st.markdown("#### Step 4: Verify Cortex Code is working")

with st.container(border=True):
    st.markdown("""
Test that Cortex Code is operational by pasting this simple prompt:

```
Show me the current role, warehouse, and database I'm using
```

You should see Cortex Code execute `SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE()`
and return your session context.
""")

st.space("small")

st.markdown("#### Lab environment details")

col1, col2, col3 = st.columns(3)
col1.metric("Duration", "3 hours", help="Total lab time including break")
col2.metric("Compute", "Pre-provisioned", help="Warehouse already configured")
col3.metric("Support", "Facilitators on-site", help="Raise your hand if stuck")
