import streamlit as st
import pandas as pd
from app.data.db import connect_database

st.set_page_config(page_title="CRUD", page_icon="⚙️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

def read_df(query, params=()):
    conn=connect_database()
    df=pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def run_sql(query, params=()):
    conn=connect_database()
    cur=conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

with st.sidebar:
    st.write("👤 Account")
    st.write(f"Username: {st.session_state.username}")
    st.write(f"Role: {str(st.session_state.role).upper()}")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in=False
        st.session_state.username=""
        st.session_state.role="user"
        st.experimental_rerun()

st.title("⚙️ CRUD Operations")

table_pick=st.selectbox("Choose section", ["🛡️ Cyber Incidents", "🛠️ IT Tickets", "📚 Datasets"], key="crud_section")
action=st.radio("Choose action", ["Create", "Read", "Update", "Delete"], horizontal=True)

st.divider()

if table_pick=="🛡️ Cyber Incidents":
    table_name="cyber_incidents"
    df=read_df("SELECT * FROM cyber_incidents ORDER BY id DESC LIMIT 200")

    if action=="Read":
        st.dataframe(df, use_container_width=True)

    elif action=="Create":
        with st.form("create_incident"):
            title=st.text_input("Title")
            severity=st.selectbox("Severity", ["low","medium","high","critical"])
            status=st.selectbox("Status", ["open","in progress","resolved"])
            submitted=st.form_submit_button("Add")

        if submitted:
            if title=="":
                st.error("Title is required")
            else:
                run_sql(
                    "INSERT INTO cyber_incidents (title, severity, status) VALUES (?, ?, ?)",
                    (title, severity, status)
                )
                st.success("Incident added")
                st.experimental_rerun()

    elif action=="Update":
        if df.empty:
            st.info("No incidents to update")
        else:
            pick_id=st.selectbox("Pick incident ID", df["id"])
            new_status=st.selectbox("New status", ["open","in progress","resolved"])
            if st.button("Update"):
                run_sql("UPDATE cyber_incidents SET status=? WHERE id=?", (new_status, int(pick_id)))
                st.success("Updated")
                st.experimental_rerun()

    else:
        if df.empty:
            st.info("No incidents to delete")
        else:
            del_id=st.selectbox("Pick incident ID to delete", df["id"], key="del_inc")
            st.warning("This cannot be undone")
            if st.button("Delete"):
                run_sql("DELETE FROM cyber_incidents WHERE id=?", (int(del_id),))
                st.success("Deleted")
                st.experimental_rerun()

elif table_pick=="🛠️ IT Tickets":
    df=read_df("SELECT * FROM it_tickets ORDER BY id DESC LIMIT 200")

    if action=="Read":
        st.dataframe(df, use_container_width=True)

    elif action=="Create":
        with st.form("create_ticket"):
            title=st.text_input("Title")
            status=st.selectbox("Status", ["open","in progress","closed"])
            priority=st.selectbox("Priority", ["low","medium","high"])
            submitted=st.form_submit_button("Add")

        if submitted:
            if title=="":
                st.error("Title is required")
            else:
                run_sql(
                    "INSERT INTO it_tickets (title, status, priority) VALUES (?, ?, ?)",
                    (title, status, priority)
                )
                st.success("Ticket added")
                st.experimental_rerun()

    elif action=="Update":
        if df.empty:
            st.info("No tickets to update")
        else:
            pick_id=st.selectbox("Pick ticket ID", df["id"])
            new_status=st.selectbox("New status", ["open","in progress","closed"])
            if st.button("Update"):
                run_sql("UPDATE it_tickets SET status=? WHERE id=?", (new_status, int(pick_id)))
                st.success("Updated")
                st.experimental_rerun()

    else:
        if df.empty:
            st.info("No tickets to delete")
        else:
            del_id=st.selectbox("Pick ticket ID to delete", df["id"], key="del_ticket")
            st.warning("This cannot be undone")
            if st.button("Delete"):
                run_sql("DELETE FROM it_tickets WHERE id=?", (int(del_id),))
                st.success("Deleted")
                st.experimental_rerun()

else:
    df=read_df("SELECT * FROM datasets_metadata ORDER BY id DESC LIMIT 200")

    if action=="Read":
        st.dataframe(df, use_container_width=True)

    elif action=="Create":
        with st.form("create_dataset"):
            name=st.text_input("Name")
            category=st.text_input("Category")
            source=st.text_input("Source")
            size=st.number_input("Size", min_value=0, step=1)
            submitted=st.form_submit_button("Add")

        if submitted:
            if name=="":
                st.error("Name is required")
            else:
                run_sql(
                    "INSERT INTO datasets_metadata (name, category, source, size) VALUES (?, ?, ?, ?)",
                    (name, category, source, int(size))
                )
                st.success("Dataset added")
                st.experimental_rerun()

    elif action=="Update":
        if df.empty:
            st.info("No datasets to update")
        else:
            pick_id=st.selectbox("Pick dataset ID", df["id"])
            new_size=st.number_input("New size", min_value=0, step=1)
            if st.button("Update"):
                run_sql("UPDATE datasets_metadata SET size=? WHERE id=?", (int(new_size), int(pick_id)))
                st.success("Updated")
                st.experimental_rerun()

    else:
        if df.empty:
            st.info("No datasets to delete")
        else:
            del_id=st.selectbox("Pick dataset ID to delete", df["id"], key="del_data")
            st.warning("This cannot be undone")
            if st.button("Delete"):
                run_sql("DELETE FROM datasets_metadata WHERE id=?", (int(del_id),))
                st.success("Deleted")
                st.experimental_rerun()
