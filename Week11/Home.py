import streamlit as st
from services.database_manager import DatabaseManager

st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Multi-Domain Intelligence Platform")
st.markdown("---")

# Initialize session state
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "current_role" not in st.session_state:
    st.session_state.current_role = None


# ✅ SIDEBAR (ONLY user info + logout) — no extra navigation buttons
st.sidebar.markdown("### 👤 Account")

if st.session_state.current_user:
    st.sidebar.success(f"Logged in as: {st.session_state.current_user}")
    st.sidebar.caption(f"Role: {st.session_state.current_role}")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.current_user = None
        st.session_state.current_role = None
        st.rerun()
else:
    st.sidebar.info("Not logged in")


# ---------------- MAIN PAGE ----------------
if st.session_state.current_user is None:
    st.info("👈 Please log in using the Login page to access the platform.")

    st.markdown("### Welcome")
    st.write("""
This platform provides:

- 🔐 Authentication  
- 🛡️ Cybersecurity incident tracking  
- 📊 Data Science dataset analysis  
- 💻 IT Operations ticketing  
- 🤖 AI Assistant
""")

else:
    st.success(
        f"✅ Logged in as **{st.session_state.current_user}** "
        f"(Role: {st.session_state.current_role})"
    )

    st.subheader("📋 Dashboard")

    db = DatabaseManager("database/platform.db")
    db.connect()

    try:
        incidents = db.fetch_one("SELECT COUNT(*) FROM security_incidents")[0]
    except:
        incidents = 0

    try:
        datasets = db.fetch_one("SELECT COUNT(*) FROM datasets")[0]
    except:
        datasets = 0

    try:
        tickets = db.fetch_one("SELECT COUNT(*) FROM it_tickets")[0]
    except:
        tickets = 0

    db.close()

    c1, c2, c3 = st.columns(3)
    c1.metric("🛡️ Incidents", incidents)
    c2.metric("📊 Datasets", datasets)
    c3.metric("💻 Tickets", tickets)

    st.markdown("---")
    st.info("Use the left sidebar pages (the top menu) to navigate.")
