import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

with st.sidebar:
    st.write("👤 Account")
    st.write(f"Username: {st.session_state.username}")
    st.write(f"Role: {str(st.session_state.role).upper()}")

st.title("⚙️ Settings")

tab1, tab2, tab3 = st.tabs(["Profile", "Preferences", "About"])

with tab1:
    st.subheader("User Profile")

    c1, c2 = st.columns(2)

    with c1:
        st.write("Username:")
        st.write(f"`{st.session_state.username}`")
        st.write("Role:")
        st.write(f"`{str(st.session_state.role).upper()}`")

    with c2:
        st.write("Account Status:")
        st.success("Active")
        st.write("Last Login:")
        st.write("N/A")

    st.divider()

    st.subheader("Security")

    if st.button("Change Password", use_container_width=True):
        st.info("Coming soon")

    if st.button("Enable Two-Factor Authentication", use_container_width=True):
        st.info("Coming soon")

with tab2:
    st.subheader("Preferences")

    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    notifications = st.checkbox("Enable Notifications", value=True)
    auto_refresh = st.checkbox("Auto-refresh Data", value=True)

    if auto_refresh:
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 300, 60)

    if st.button("Save Preferences", use_container_width=True):
        st.success("Preferences saved!")

with tab3:
    st.subheader("About")

    st.markdown("""
### Multi-Domain Intelligence Platform

Version: Week 9

Technology:
- Streamlit
- Python
- SQLite
- Plotly
""")
