import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket

st.set_page_config(
    page_title="IT Operations - Multi-Domain Platform",
    page_icon="💻",
    layout="wide"
)

st.title("💻 IT Operations")
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
tab1, tab2, tab3 = st.tabs(["View Tickets", "Create Ticket", "Statistics"])

with tab1:
    st.subheader("Support Tickets")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])
    
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
    
    with col3:
        st.empty()
    
    # Fetch tickets from database
    try:
        rows = db.fetch_all("SELECT id, title, priority, status, assigned_to FROM it_tickets")
        
        if rows:
            tickets = []
            for row in rows:
                ticket = ITTicket(
                    ticket_id=row[0],
                    title=row[1],
                    priority=row[2],
                    status=row[3],
                    assigned_to=row[4]
                )
                tickets.append(ticket)
            
            # Filter tickets
            filtered_tickets = tickets
            if priority_filter != "All":
                filtered_tickets = [t for t in filtered_tickets if t.get_priority() == priority_filter]
            if status_filter != "All":
                filtered_tickets = [t for t in filtered_tickets if t.get_status() == status_filter]
            
            # Display tickets
            if filtered_tickets:
                for ticket in filtered_tickets:
                    with st.container(border=True):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Ticket ID", ticket.get_id())
                        
                        with col2:
                            priority_color = {
                                "Low": "🟢",
                                "Medium": "🟡",
                                "High": "🟠",
                                "Critical": "🔴"
                            }
                            color = priority_color.get(ticket.get_priority(), "⚪")
                            st.metric("Priority", f"{color} {ticket.get_priority()}")
                        
                        with col3:
                            st.metric("Status", ticket.get_status())
                        
                        with col4:
                            st.metric("Assigned To", ticket.get_assigned_to() or "Unassigned")
                        
                        st.write(f"**Title:** {ticket.get_title()}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"👤 Assign", key=f"assign_{ticket.get_id()}"):
                                staff_member = st.text_input("Assign to staff member:", key=f"staff_{ticket.get_id()}")
                                if staff_member:
                                    ticket.assign_to(staff_member)
                                    db.execute_query(
                                        "UPDATE it_tickets SET assigned_to = ? WHERE id = ?",
                                        (staff_member, ticket.get_id())
                                    )
                                    st.success(f"✅ Ticket assigned to {staff_member}")
                                    st.rerun()
                        
                        with col2:
                            if st.button(f"✅ Mark Resolved", key=f"resolve_{ticket.get_id()}"):
                                db.execute_query(
                                    "UPDATE it_tickets SET status = ? WHERE id = ?",
                                    ("Resolved", ticket.get_id())
                                )
                                st.success(f"✅ Ticket marked as Resolved")
                                st.rerun()
                        
                        with col3:
                            if ticket.get_status() != "Closed":
                                if st.button(f"🔒 Close Ticket", key=f"close_{ticket.get_id()}"):
                                    ticket.close_ticket()
                                    db.execute_query(
                                        "UPDATE it_tickets SET status = ? WHERE id = ?",
                                        ("Closed", ticket.get_id())
                                    )
                                    st.success(f"✅ Ticket closed")
                                    st.rerun()
            else:
                st.info("No tickets match the selected filters")
        else:
            st.info("📋 No support tickets yet")
    
    except Exception as e:
        st.error(f"Error fetching tickets: {e}")

with tab2:
    st.subheader("Create New Ticket")
    
    title = st.text_input("Ticket Title", placeholder="Brief description of the issue")
    
    col1, col2 = st.columns(2)
    with col1:
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    
    with col2:
        assigned_to = st.text_input("Assigned To (optional)", placeholder="Staff member name")
    
    description = st.text_area("Description", placeholder="Detailed description of the issue", height=150)
    
    if st.button("🎫 Create Ticket", use_container_width=True):
        if not title or not description:
            st.error("❌ Please fill in title and description")
        else:
            try:
                db.execute_query(
                    "INSERT INTO it_tickets (title, priority, status, assigned_to) VALUES (?, ?, ?, ?)",
                    (title, priority, "Open", assigned_to if assigned_to else None)
                )
                st.success(f"✅ Ticket created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating ticket: {e}")

with tab3:
    st.subheader("Ticket Statistics")
    
    try:
        # Count tickets by priority
        priority_stats = {}
        for priority in ["Low", "Medium", "High", "Critical"]:
            count = db.fetch_one(
                "SELECT COUNT(*) FROM it_tickets WHERE priority = ?",
                (priority,)
            )[0]
            priority_stats[priority] = count
        
        # Count tickets by status
        status_stats = {}
        for status in ["Open", "In Progress", "Resolved", "Closed"]:
            count = db.fetch_one(
                "SELECT COUNT(*) FROM it_tickets WHERE status = ?",
                (status,)
            )[0]
            status_stats[status] = count
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Tickets", sum(priority_stats.values()))
            st.bar_chart(priority_stats)
            st.caption("Tickets by Priority")
        
        with col2:
            st.metric("Open Tickets", status_stats.get("Open", 0))
            st.bar_chart(status_stats)
            st.caption("Tickets by Status")
        
        st.markdown("---")
        
        # Average resolution time (if updated_at is tracked)
        st.metric("System Status", "✅ All Systems Operational")
    
    except Exception as e:
        st.error(f"Error loading statistics: {e}")

db.close()