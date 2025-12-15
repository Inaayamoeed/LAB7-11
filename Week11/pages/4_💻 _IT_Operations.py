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

st.success("Logged in as: {}".format(st.session_state.current_user))

db = DatabaseManager("database/platform.db")
db.connect()

try:
    tab1, tab2, tab3 = st.tabs(["View Tickets", "Create Ticket", "Statistics"])

    # =========================
    # TAB 1: VIEW TICKETS
    # =========================
    with tab1:
        st.subheader("Support Tickets")

        col1, col2, col3 = st.columns(3)
        with col1:
            priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
        with col3:
            st.empty()

        try:
            rows = db.fetch_all("SELECT id, title, priority, status, assigned_to FROM it_tickets")

            if not rows:
                st.info("📋 No support tickets yet")
            else:
                tickets = []
                for row in rows:
                    tickets.append(
                        ITTicket(
                            ticket_id=row[0],
                            title=row[1],
                            priority=row[2],
                            status=row[3],
                            assigned_to=row[4]
                        )
                    )

                filtered = tickets
                if priority_filter != "All":
                    filtered = [t for t in filtered if (t.get_priority() or "") == priority_filter]
                if status_filter != "All":
                    filtered = [t for t in filtered if (t.get_status() or "") == status_filter]

                if not filtered:
                    st.info("No tickets match the selected filters")
                else:
                    for ticket in filtered:
                        with st.container():  # ✅ no border=True
                            c1, c2, c3, c4 = st.columns(4)

                            with c1:
                                st.metric("Ticket ID", ticket.get_id())
                            with c2:
                                priority_color = {
                                    "Low": "🟢",
                                    "Medium": "🟡",
                                    "High": "🟠",
                                    "Critical": "🔴"
                                }
                                color = priority_color.get(ticket.get_priority(), "⚪")
                                st.metric("Priority", "{} {}".format(color, ticket.get_priority() or "Unknown"))
                            with c3:
                                st.metric("Status", ticket.get_status() or "Unknown")
                            with c4:
                                st.metric("Assigned To", ticket.get_assigned_to() or "Unassigned")

                            st.write("**Title:** {}".format(ticket.get_title() or ""))

                            a1, a2, a3 = st.columns(3)

                            with a1:
                                with st.expander("👤 Assign"):
                                    staff_member = st.text_input(
                                        "Assign to staff member:",
                                        key="staff_{}".format(ticket.get_id())
                                    )
                                    if st.button("Save Assignment", key="save_assign_{}".format(ticket.get_id())):
                                        if not staff_member:
                                            st.error("❌ Please enter a staff member name")
                                        else:
                                            db.execute_query(
                                                "UPDATE it_tickets SET assigned_to = ? WHERE id = ?",
                                                (staff_member, ticket.get_id())
                                            )
                                            st.success("✅ Ticket assigned to {}".format(staff_member))
                                            st.experimental_rerun()

                            with a2:
                                if st.button("✅ Mark Resolved", key="resolve_{}".format(ticket.get_id())):
                                    db.execute_query(
                                        "UPDATE it_tickets SET status = ? WHERE id = ?",
                                        ("Resolved", ticket.get_id())
                                    )
                                    st.success("✅ Ticket marked as Resolved")
                                    st.experimental_rerun()

                            with a3:
                                if (ticket.get_status() or "") != "Closed":
                                    if st.button("🔒 Close Ticket", key="close_{}".format(ticket.get_id())):
                                        db.execute_query(
                                            "UPDATE it_tickets SET status = ? WHERE id = ?",
                                            ("Closed", ticket.get_id())
                                        )
                                        st.success("✅ Ticket closed")
                                        st.experimental_rerun()

                        st.markdown("---")

        except Exception as e:
            st.error("Error fetching tickets: {}".format(e))

    # =========================
    # TAB 2: CREATE TICKET
    # =========================
    with tab2:
        st.subheader("Create New Ticket")

        title = st.text_input("Ticket Title", value="")

        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        with col2:
            assigned_to = st.text_input("Assigned To (optional)", value="")

        if st.button("🎫 Create Ticket", use_container_width=True):
            if not title:
                st.error("❌ Please fill in title")
            else:
                try:
                    db.execute_query(
                        "INSERT INTO it_tickets (title, priority, status, assigned_to) VALUES (?, ?, ?, ?)",
                        (title, priority, "Open", assigned_to if assigned_to else None)
                    )
                    st.success("✅ Ticket created successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error("Error creating ticket: {}".format(e))

    # =========================
    # TAB 3: STATISTICS
    # =========================
    with tab3:
        st.subheader("Ticket Statistics")

        try:
            priority_stats = {}
            for p in ["Low", "Medium", "High", "Critical"]:
                priority_stats[p] = db.fetch_one(
                    "SELECT COUNT(*) FROM it_tickets WHERE priority = ?",
                    (p,)
                )[0]

            status_stats = {}
            for s in ["Open", "In Progress", "Resolved", "Closed"]:
                status_stats[s] = db.fetch_one(
                    "SELECT COUNT(*) FROM it_tickets WHERE status = ?",
                    (s,)
                )[0]

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
            st.metric("System Status", "✅ All Systems Operational")

        except Exception as e:
            st.error("Error loading statistics: {}".format(e))

finally:
    db.close()
