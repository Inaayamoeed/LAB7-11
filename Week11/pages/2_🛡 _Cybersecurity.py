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

st.success(f"Logged in as: {st.session_state.current_user}")

# Initialize database
db = DatabaseManager("database/platform.db")
db.connect()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["View Incidents", "Add Incident", "Statistics"])

with tab1:
    st.subheader("Security Incidents")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity_filter = st.selectbox("Filter by Severity", ["All", "low", "medium", "high", "critical"])
    
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
    
    with col3:
        st.empty()
    
    # Fetch incidents from database
    try:
        rows = db.fetch_all("SELECT id, incident_type, severity, status, description FROM security_incidents")
        
        if rows:
            incidents = []
            for row in rows:
                incident = SecurityIncident(
                    incident_id=row[0],
                    incident_type=row[1],
                    severity=row[2],
                    status=row[3],
                    description=row[4]
                )
                incidents.append(incident)
            
            # Filter incidents
            filtered_incidents = incidents
            if severity_filter != "All":
                filtered_incidents = [i for i in filtered_incidents if i.get_severity().lower() == severity_filter.lower()]
            if status_filter != "All":
                filtered_incidents = [i for i in filtered_incidents if i.get_status() == status_filter]
            
            # Display incidents
            if filtered_incidents:
                for incident in filtered_incidents:
                    with st.container(border=True):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("ID", incident.get_id())
                        
                        with col2:
                            severity_level = incident.get_severity_level()
                            st.metric("Severity", f"{incident.get_severity().upper()} ({severity_level}/4)")
                        
                        with col3:
                            st.metric("Type", incident.get_incident_type())
                        
                        with col4:
                            st.metric("Status", incident.get_status())
                        
                        st.write(f"**Description:** {incident.get_description()}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"Update Status", key=f"update_{incident.get_id()}"):
                                new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"], key=f"status_{incident.get_id()}")
                                incident.update_status(new_status)
                                db.execute_query(
                                    "UPDATE security_incidents SET status = ? WHERE id = ?",
                                    (new_status, incident.get_id())
                                )
                                st.success(f"✅ Incident {incident.get_id()} updated to {new_status}")
                                st.experimental_rerun()
            else:
                st.info("No incidents match the selected filters")
        else:
            st.info("📋 No security incidents recorded yet")
    
    except Exception as e:
        st.error(f"Error fetching incidents: {e}")

with tab2:
    st.subheader("Report New Incident")
    
    incident_type = st.selectbox("Incident Type", [
        "Malware Detection",
        "Unauthorized Access",
        "Data Breach",
        "DDoS Attack",
        "Phishing",
        "Configuration Error",
        "Other"
    ])
    
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
                st.success(f"✅ Incident reported successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error reporting incident: {e}")

with tab3:
    st.subheader("Security Statistics")
    
    try:
        # Count incidents by severity
        severity_stats = {}
        for severity in ["low", "medium", "high", "critical"]:
            count = db.fetch_one(
                "SELECT COUNT(*) FROM security_incidents WHERE severity = ?",
                (severity,)
            )[0]
            severity_stats[severity] = count
        
        # Count incidents by status
        status_stats = {}
        for status in ["Open", "In Progress", "Resolved", "Closed"]:
            count = db.fetch_one(
                "SELECT COUNT(*) FROM security_incidents WHERE status = ?",
                (status,)
            )[0]
            status_stats[status] = count
        
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
        st.error(f"Error loading statistics: {e}")

db.close()
