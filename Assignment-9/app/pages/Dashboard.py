import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.db import connect_database

st.set_page_config(page_title="Dashboard", page_icon="🧩", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

def read_table(sql):
    conn=connect_database()
    df=pd.read_sql_query(sql, conn)
    conn.close()
    return df

def lower_col(df, col):
    return df[col].astype(str).str.lower() if col in df.columns else pd.Series([], dtype=str)

with st.sidebar:
    st.write("👤 Account")
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {str(st.session_state.role).upper()}")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in=False
        st.session_state.username=""
        st.session_state.role="user"
        st.experimental_rerun()

st.title("🧩 Multi-Domain Dashboard")

top1, top2, top3=st.columns([2, 1, 1])
with top2:
    chart_style=st.selectbox("Chart style", ["Bar", "Pie", "Line"], key="chart_style")
with top3:
    row_limit=st.selectbox("Rows", [50, 100, 200], key="row_limit")

tab_a, tab_b, tab_c=st.tabs(["🛡️ Security", "🛠️ IT Ops", "📚 Data"])

with tab_a:
    st.subheader("🛡️ Cyber Incidents")
    df=read_table(f"SELECT * FROM cyber_incidents LIMIT {row_limit}")

    if df.empty:
        st.warning("No incidents data available")
    else:
        a1, a2, a3, a4=st.columns(4)
        a1.metric("Incidents", len(df))
        a2.metric("Critical", int((lower_col(df, "severity")=="critical").sum()) if "severity" in df.columns else 0)
        a3.metric("High", int((lower_col(df, "severity")=="high").sum()) if "severity" in df.columns else 0)
        a4.metric("Resolved", int((lower_col(df, "status")=="resolved").sum()) if "status" in df.columns else 0)

        st.divider()

        left, right=st.columns(2)

        with left:
            st.write("Severity summary")
            if "severity" in df.columns:
                counts=df["severity"].value_counts()
                if chart_style=="Bar":
                    fig=px.bar(x=counts.index, y=counts.values, labels={"x":"Severity","y":"Count"})
                elif chart_style=="Pie":
                    fig=px.pie(values=counts.values, names=counts.index)
                else:
                    fig=px.line(x=counts.index, y=counts.values, markers=True, labels={"x":"Severity","y":"Count"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No severity column found.")

        with right:
            st.write("Status summary")
            if "status" in df.columns:
                counts=df["status"].value_counts()
                fig=px.pie(values=counts.values, names=counts.index)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No status column found.")

        with st.expander("📋 View incidents table"):
            st.dataframe(df, use_container_width=True)

with tab_b:
    st.subheader("🛠️ IT Tickets")
    df=read_table(f"SELECT * FROM it_tickets LIMIT {row_limit}")

    if df.empty:
        st.warning("No tickets data available")
    else:
        b1, b2, b3, b4=st.columns(4)
        b1.metric("Tickets", len(df))
        b2.metric("Open", int((lower_col(df, "status")=="open").sum()) if "status" in df.columns else 0)
        b3.metric("In Progress", int((lower_col(df, "status")=="in progress").sum()) if "status" in df.columns else 0)
        b4.metric("Closed", int((lower_col(df, "status")=="closed").sum()) if "status" in df.columns else 0)

        st.divider()

        left, right=st.columns(2)

        with left:
            st.write("Ticket status")
            if "status" in df.columns:
                counts=df["status"].value_counts()
                if chart_style=="Bar":
                    fig=px.bar(x=counts.index, y=counts.values, labels={"x":"Status","y":"Count"})
                elif chart_style=="Pie":
                    fig=px.pie(values=counts.values, names=counts.index)
                else:
                    fig=px.line(x=counts.index, y=counts.values, markers=True, labels={"x":"Status","y":"Count"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No status column found.")

        with right:
            st.write("Priority split")
            if "priority" in df.columns:
                counts=df["priority"].value_counts()
                fig=px.pie(values=counts.values, names=counts.index)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No priority column found.")

        with st.expander("📋 View tickets table"):
            st.dataframe(df, use_container_width=True)

with tab_c:
    st.subheader("📚 Datasets")
    df=read_table(f"SELECT * FROM datasets_metadata LIMIT {row_limit}")

    if df.empty:
        st.warning("No datasets data available")
    else:
        c1, c2, c3, c4=st.columns(4)
        c1.metric("Datasets", len(df))
        c2.metric("Categories", df["category"].nunique() if "category" in df.columns else 0)
        c3.metric("Sources", df["source"].nunique() if "source" in df.columns else 0)
        c4.metric("Records", len(df))

        st.divider()

        left, right=st.columns(2)

        with left:
            st.write("By category")
            if "category" in df.columns:
                counts=df["category"].value_counts()
                if chart_style=="Bar":
                    fig=px.bar(x=counts.index, y=counts.values, labels={"x":"Category","y":"Count"})
                elif chart_style=="Pie":
                    fig=px.pie(values=counts.values, names=counts.index)
                else:
                    fig=px.line(x=counts.index, y=counts.values, markers=True, labels={"x":"Category","y":"Count"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No category column found.")

        with right:
            st.write("By source")
            if "source" in df.columns:
                counts=df["source"].value_counts()
                fig=px.pie(values=counts.values, names=counts.index)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No source column found.")

        with st.expander("📋 View datasets table"):
            st.dataframe(df, use_container_width=True)
