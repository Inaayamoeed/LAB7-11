import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident

st.set_page_config(
    page_title="Cybersecurity - Multi-Domain Platform",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Cybersecurity Incidents")
st.markdown("---")

# Check if logged in
if not st.session_state.get("current_user"):
    st.warning("⚠️ Please login first")
    st.stop()

st.success("Logged in as: {}".format(st.session_state.current_user))

db = DatabaseManager("database/platform.db")
db.connect()

try:
    tab1, tab2, tab3 = st.tabs(["View Incidents", "Add Incident", "Statistics"])

    # =========================
    # TAB 1: VIEW INCIDENTS
    # =========================
    with tab1:
        st.subheader("Security Incidents")

        col1, col2, col3 = st.columns(3)
        with col1:
            severity_filter = st.selectbox(
                "Filter by Severity",
                ["All", "low", "medium", "high", "critical"]
            )
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Open", "In Progress", "Resolved", "Closed"]
            )
        with col3:
            st.empty()

        try:
            rows = db.fetch_all("SELECT id, incident_type, severity, status, description FROM security_incidents")

            if not rows:
                st.info("📋 No security incidents recorded yet")
            else:
                incidents = []
                for row in rows:
                    incidents.append(
                        SecurityIncident(
                            incident_id=row[0],
                            incident_type=row[1],
                            severity=row[2],
                            status=row[3],
                            description=row[4]
                        )
                    )

                filtered = incidents

                if severity_filter != "All":
                    filtered = [
                        i for i in filtered
                        if (i.get_severity() or "").lower() == severity_filter.lower()
                    ]

                if status_filter != "All":
                    filtered = [
                        i for i in filtered
                        if (i.get_status() or "").strip().lower() == status_filter.strip().lower()
                    ]

                if not filtered:
                    st.info("No incidents match the selected filters")
                else:
                    for incident in filtered:
                        # ✅ FIX: no border=True (older Streamlit)
                        with st.container():
                            c1, c2, c3, c4 = st.columns(4)

                            with c1:
                                st.metric("ID", incident.get_id())

                            with c2:
                                severity_level = incident.get_severity_level()
                                sev_text = (incident.get_severity() or "Unknown").upper()
                                st.metric("Severity", "{} ({}/4)".format(sev_text, severity_level))

                            with c3:
                                st.metric("Type", incident.get_incident_type() or "Unknown")

                            with c4:
                                st.metric("Status", incident.get_status() or "Unknown")

                            st.write("**Description:** {}".format(incident.get_description() or ""))

                            with st.expander("Update Status"):
                                status_options = ["Open", "In Progress", "Resolved", "Closed"]
                                current_status = (incident.get_status() or "Open").strip()

                                index_val = 0
                                if current_status in status_options:
                                    index_val = status_options.index(current_status)

                                new_status = st.selectbox(
                                    "New Status",
                                    status_options,
                                    index=index_val,
                                    key="status_select_{}".format(incident.get_id())
                                )

                                if st.button("Save Status", key="save_status_{}".format(incident.get_id())):
                                    db.execute_query(
                                        "UPDATE security_incidents SET status = ? WHERE id = ?",
                                        (new_status, incident.get_id())
                                    )
                                    st.success("✅ Incident {} updated to {}".format(incident.get_id(), new_status))
                                    st.experimental_rerun()

                        st.markdown("---")

        except Exception as e:
            st.error("Error fetching incidents: {}".format(e))

    # =========================
    # TAB 2: ADD INCIDENT
    # =========================
    with tab2:
        st.subheader("Report New Incident")

        incident_type = st.selectbox(
            "Incident Type",
            [
                "Malware Detection",
                "Unauthorized Access",
                "Data Breach",
                "DDoS Attack",
                "Phishing",
                "Configuration Error",
                "Other"
            ]
        )

        severity = st.selectbox("Severity Level", ["low", "medium", "high", "critical"])
        description = st.text_area("Description", placeholder="Describe the incident in detail...")

        if st.button("🚨 Report Incident", use_container_width=True):
            if not description:
                st.error("❌ Please provide a description")
            else:
                try:
                    db.execute_query(
                        "INSERT INTO security_incidents (incident_type, severity, status, description) VALUES (?, ?, ?, ?)",
                        (incident_type, severity, "Open", description)
                    )
                    st.success("✅ Incident reported successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error("Error reporting incident: {}".format(e))

    # =========================
    # TAB 3: STATISTICS
    # =========================
    with tab3:
        st.subheader("Security Statistics")

        try:
            severity_stats = {}
            for sev in ["low", "medium", "high", "critical"]:
                severity_stats[sev] = db.fetch_one(
                    "SELECT COUNT(*) FROM security_incidents WHERE LOWER(severity) = ?",
                    (sev,)
                )[0]

            status_stats = {}
            for status in ["Open", "In Progress", "Resolved", "Closed"]:
                status_stats[status] = db.fetch_one(
                    "SELECT COUNT(*) FROM security_incidents WHERE status = ?",
                    (status,)
                )[0]

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total Incidents", sum(severity_stats.values()))
                st.bar_chart(severity_stats)
                st.caption("Incidents by Severity")

            with col2:
                st.metric("Open Incidents", status_stats.get("Open", 0))
                st.bar_chart(status_stats)
                st.caption("Incidents by Status")

        except Exception as e:
            st.error("Error loading statistics: {}".format(e))

finally:
    db.close()
