import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.db import connect_database

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

def load_df(query):
    conn=connect_database()
    df=pd.read_sql_query(query, conn)
    conn.close()
    return df

def safe_lower(series):
    return series.astype(str).str.lower()

with st.sidebar:
    st.write("👤 Account")
    st.write(f"Username: {st.session_state.username}")
    st.write(f"Role: {str(st.session_state.role).upper()}")

st.title("📈 Analytics & Reporting")

users_df=load_df("SELECT * FROM users")
incidents_df=load_df("SELECT * FROM cyber_incidents")
tickets_df=load_df("SELECT * FROM it_tickets")
datasets_df=load_df("SELECT * FROM datasets_metadata")

m1, m2, m3, m4=st.columns(4)
m1.metric("Users", len(users_df))
m2.metric("Incidents", len(incidents_df))
m3.metric("Tickets", len(tickets_df))
m4.metric("Datasets", len(datasets_df))

st.divider()

tab1, tab2, tab3=st.tabs(["🧑 Users", "🛡️ Incidents", "🧾 Tickets"])

with tab1:
    st.subheader("Users Overview")

    if users_df.empty or "role" not in users_df.columns:
        st.info("No user role data found.")
    else:
        role_counts=users_df["role"].value_counts()
        left, right=st.columns(2)

        with left:
            chart=st.selectbox("User chart", ["Bar", "Pie"], key="users_chart")
            if chart=="Bar":
                fig=px.bar(x=role_counts.index, y=role_counts.values, labels={"x":"Role","y":"Count"})
            else:
                fig=px.pie(values=role_counts.values, names=role_counts.index)
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.dataframe(role_counts.reset_index().rename(columns={"index":"role","role":"count"}), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Incidents Overview")

    if incidents_df.empty:
        st.warning("No incidents found.")
    else:
        col1, col2=st.columns(2)

        with col1:
            if "severity" in incidents_df.columns:
                sev_counts=incidents_df["severity"].value_counts()
                chart=st.selectbox("Severity chart", ["Bar", "Pie", "Line"], key="sev_chart")
                if chart=="Bar":
                    fig=px.bar(x=sev_counts.index, y=sev_counts.values, labels={"x":"Severity","y":"Count"})
                elif chart=="Pie":
                    fig=px.pie(values=sev_counts.values, names=sev_counts.index)
                else:
                    fig=px.line(x=sev_counts.index, y=sev_counts.values, markers=True, labels={"x":"Severity","y":"Count"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No severity column found.")

        with col2:
            if "status" in incidents_df.columns:
                status_counts=incidents_df["status"].value_counts()
                fig=px.pie(values=status_counts.values, names=status_counts.index)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No status column found.")

        with st.expander("📄 Show incidents table"):
            st.dataframe(incidents_df, use_container_width=True)

with tab3:
    st.subheader("Tickets Overview")

    if tickets_df.empty:
        st.warning("No tickets found.")
    else:
        left, right=st.columns(2)

        with left:
            if "priority" in tickets_df.columns:
                pr_counts=tickets_df["priority"].value_counts()
                chart=st.selectbox("Priority chart", ["Bar", "Pie"], key="priority_chart")
                if chart=="Bar":
                    fig=px.bar(x=pr_counts.index, y=pr_counts.values, labels={"x":"Priority","y":"Count"})
                else:
                    fig=px.pie(values=pr_counts.values, names=pr_counts.index)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No priority column found.")

        with right:
            if "status" in tickets_df.columns:
                st_counts=tickets_df["status"].value_counts()
                chart=st.selectbox("Status chart", ["Bar", "Pie", "Line"], key="ticket_status_chart")
                if chart=="Bar":
                    fig=px.bar(x=st_counts.index, y=st_counts.values, labels={"x":"Status","y":"Count"})
                elif chart=="Pie":
                    fig=px.pie(values=st_counts.values, names=st_counts.index)
                else:
                    fig=px.line(x=st_counts.index, y=st_counts.values, markers=True, labels={"x":"Status","y":"Count"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No status column found.")

        with st.expander("📄 Show tickets table"):
            st.dataframe(tickets_df, use_container_width=True)
