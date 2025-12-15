import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database_manager import DatabaseManager
from models.dataset import Dataset


# ---------- small helpers (older Streamlit safe) ----------
def do_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def safe_int(x, default=0):
    try:
        if x is None:
            return default
        return int(x)
    except Exception:
        return default


st.set_page_config(
    page_title="Data Science - Multi-Domain Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Science")
st.markdown("---")

# Check login
if not st.session_state.get("current_user"):
    st.warning("⚠️ Please login first")
    st.stop()

st.success("Logged in as: {}".format(st.session_state.current_user))

# Connect DB
db = DatabaseManager("database/platform.db")
db.connect()

try:
    # ✅ Tabs if your Streamlit supports it, otherwise sidebar menu
    use_tabs = hasattr(st, "tabs")

    if use_tabs:
        tab1, tab2, tab3 = st.tabs(["View Datasets", "Upload Dataset", "Analysis"])
        sections = [("View Datasets", tab1), ("Upload Dataset", tab2), ("Analysis", tab3)]
    else:
        st.sidebar.header("📌 Data Science Menu")
        choice = st.sidebar.selectbox("Choose section", ["View Datasets", "Upload Dataset", "Analysis"])
        sections = [(choice, st)]

    for section_name, ui in sections:

        # ---------------- VIEW DATASETS ----------------
        if section_name == "View Datasets":
            with ui:
                st.subheader("Available Datasets")

                col1, col2 = st.columns(2)
                with col1:
                    sort_by = st.selectbox("Sort by", ["Name", "Size", "Rows"])
                with col2:
                    st.empty()

                try:
                    rows = db.fetch_all("SELECT id, name, size_bytes, rows, source FROM datasets")

                    if not rows:
                        st.info("📋 No datasets uploaded yet")
                    else:
                        datasets = []
                        for row in rows:
                            datasets.append(
                                Dataset(
                                    dataset_id=row[0],
                                    name=row[1],
                                    size_bytes=row[2],
                                    rows=row[3],
                                    source=row[4]
                                )
                            )

                        # Sort datasets
                        if sort_by == "Size":
                            datasets.sort(key=lambda x: float(x.calculate_size_mb() or 0), reverse=True)
                        elif sort_by == "Rows":
                            datasets.sort(key=lambda x: safe_int(x.get_rows(), 0), reverse=True)
                        else:
                            datasets.sort(key=lambda x: (x.get_name() or "").lower())

                        for dataset in datasets:
                            # ✅ No border=True (older streamlit safe)
                            with st.container():
                                c1, c2, c3, c4 = st.columns(4)

                                with c1:
                                    st.write("**Dataset ID**")
                                    st.write(dataset.get_id())

                                with c2:
                                    st.write("**Size**")
                                    st.write("{:.2f} MB".format(float(dataset.calculate_size_mb() or 0)))

                                with c3:
                                    st.write("**Rows**")
                                    st.write("{:,}".format(safe_int(dataset.get_rows(), 0)))

                                with c4:
                                    st.write("**Source**")
                                    st.write(dataset.get_source() or "Unknown")

                                st.write("**Name:** {}".format(dataset.get_name() or "Unknown"))

                                with st.expander("📥 View Details"):
                                    st.write("- **Name:** {}".format(dataset.get_name() or "Unknown"))
                                    st.write("- **Size:** {:.2f} MB ({:.4f} GB)".format(
                                        float(dataset.calculate_size_mb() or 0),
                                        float(dataset.calculate_size_gb() or 0)
                                    ))
                                    st.write("- **Rows:** {:,}".format(safe_int(dataset.get_rows(), 0)))
                                    st.write("- **Source:** {}".format(dataset.get_source() or "Unknown"))
                                    st.write("- **ID:** {}".format(dataset.get_id()))

                                st.markdown("---")

                except Exception as e:
                    st.error("Error fetching datasets: {}".format(e))

        # ---------------- UPLOAD DATASET ----------------
        elif section_name == "Upload Dataset":
            with ui:
                st.subheader("Upload New Dataset")

                dataset_name = st.text_input("Dataset Name", value="")
                dataset_source = st.text_input("Data Source", value="")

                col1, col2 = st.columns(2)
                with col1:
                    size_mb = st.number_input("Size (MB)", min_value=0.1, value=1.0)
                with col2:
                    num_rows = st.number_input("Number of Rows", min_value=1, value=1000)

                if st.button("📤 Upload Dataset"):
                    if not dataset_name or not dataset_source:
                        st.error("❌ Please fill in all fields")
                    else:
                        try:
                            size_bytes = int(float(size_mb) * 1024 * 1024)
                            db.execute_query(
                                "INSERT INTO datasets (name, size_bytes, rows, source) VALUES (?, ?, ?, ?)",
                                (dataset_name, size_bytes, int(num_rows), dataset_source)
                            )
                            st.success("✅ Dataset '{}' uploaded successfully!".format(dataset_name))
                            do_rerun()
                        except Exception as e:
                            st.error("Error uploading dataset: {}".format(e))

        # ---------------- ANALYSIS ----------------
        elif section_name == "Analysis":
            with ui:
                st.subheader("Data Analysis")

                try:
                    rows = db.fetch_all("SELECT id, name, size_bytes, rows, source FROM datasets")

                    if not rows:
                        st.info("📊 No data to analyze yet. Upload datasets first!")
                    else:
                        total_size_bytes = sum(safe_int(r[2], 0) for r in rows)
                        total_rows = sum(safe_int(r[3], 0) for r in rows)
                        num_datasets = len(rows)

                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Total Datasets", num_datasets)
                        c2.metric("Total Size", "{:.2f} GB".format(total_size_bytes / (1024**3)))
                        c3.metric("Total Rows", "{:,}".format(total_rows))

                        avg_size = (total_size_bytes / num_datasets) if num_datasets > 0 else 0
                        c4.metric("Avg Size", "{:.2f} MB".format(avg_size / (1024**2)))

                        st.markdown("---")

                        dataset_names = [(r[1] or "Unknown") for r in rows]
                        dataset_sizes = [safe_int(r[2], 0) / (1024**2) for r in rows]  # MB
                        dataset_rows = [safe_int(r[3], 0) for r in rows]

                        st.subheader("Dataset Size Distribution")
                        chart_data = pd.DataFrame({"Dataset": dataset_names, "Size (MB)": dataset_sizes})
                        st.bar_chart(chart_data.set_index("Dataset"))

                        st.subheader("Row Count by Dataset")
                        chart_data2 = pd.DataFrame({"Dataset": dataset_names, "Rows": dataset_rows})
                        st.line_chart(chart_data2.set_index("Dataset"))

                except Exception as e:
                    st.error("Error loading analysis: {}".format(e))

finally:
    db.close()
