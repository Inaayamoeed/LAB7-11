import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database_manager import DatabaseManager
from models.dataset import Dataset

st.set_page_config(
    page_title="Data Science - Multi-Domain Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Science")
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
tab1, tab2, tab3 = st.tabs(["View Datasets", "Upload Dataset", "Analysis"])

with tab1:
    st.subheader("Available Datasets")
    
    # Sort options
    col1, col2 = st.columns(2)
    
    with col1:
        sort_by = st.selectbox("Sort by", ["Name", "Size", "Rows"])
    
    with col2:
        st.empty()
    
    try:
        rows = db.fetch_all("SELECT id, name, size_bytes, rows, source FROM datasets")
        
        if rows:
            datasets = []
            for row in rows:
                dataset = Dataset(
                    dataset_id=row[0],
                    name=row[1],
                    size_bytes=row[2],
                    rows=row[3],
                    source=row[4]
                )
                datasets.append(dataset)
            
            # Sort datasets
            if sort_by == "Size":
                datasets.sort(key=lambda x: x.calculate_size_mb(), reverse=True)
            elif sort_by == "Rows":
                datasets.sort(key=lambda x: x.get_rows(), reverse=True)
            else:
                datasets.sort(key=lambda x: x.get_name())
            
            # Display datasets
            for dataset in datasets:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Dataset ID", dataset.get_id())
                    
                    with col2:
                        st.metric("Size", f"{dataset.calculate_size_mb():.2f} MB")
                    
                    with col3:
                        st.metric("Rows", f"{dataset.get_rows():,}")
                    
                    with col4:
                        st.metric("Source", dataset.get_source())
                    
                    st.write(f"**Name:** {dataset.get_name()}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📥 View Details", key=f"view_{dataset.get_id()}"):
                            st.info(f"""
                            **Dataset Details:**
                            - Name: {dataset.get_name()}
                            - Size: {dataset.calculate_size_mb():.2f} MB ({dataset.calculate_size_gb():.4f} GB)
                            - Rows: {dataset.get_rows():,}
                            - Source: {dataset.get_source()}
                            - ID: {dataset.get_id()}
                            """)
        else:
            st.info("📋 No datasets uploaded yet")
    
    except Exception as e:
        st.error(f"Error fetching datasets: {e}")

with tab2:
    st.subheader("Upload New Dataset")
    
    dataset_name = st.text_input("Dataset Name", placeholder="e.g., Customer Sales Data")
    dataset_source = st.text_input("Data Source", placeholder="e.g., CSV file, API, Database")
    
    col1, col2 = st.columns(2)
    with col1:
        size_mb = st.number_input("Size (MB)", min_value=0.1, value=1.0)
    
    with col2:
        num_rows = st.number_input("Number of Rows", min_value=1, value=1000)
    
    if st.button("📤 Upload Dataset", use_container_width=True):
        if not dataset_name or not dataset_source:
            st.error("❌ Please fill in all fields")
        else:
            try:
                size_bytes = int(size_mb * 1024 * 1024)
                db.execute_query(
                    "INSERT INTO datasets (name, size_bytes, rows, source) VALUES (?, ?, ?, ?)",
                    (dataset_name, size_bytes, num_rows, dataset_source)
                )
                st.success(f"✅ Dataset '{dataset_name}' uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error uploading dataset: {e}")

with tab3:
    st.subheader("Data Analysis")
    
    try:
        rows = db.fetch_all("SELECT id, name, size_bytes, rows, source FROM datasets")
        
        if rows:
            total_size_bytes = sum(row[2] for row in rows)
            total_rows = sum(row[3] for row in rows)
            num_datasets = len(rows)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Datasets", num_datasets)
            
            with col2:
                st.metric("Total Size", f"{total_size_bytes / (1024**3):.2f} GB")
            
            with col3:
                st.metric("Total Rows", f"{total_rows:,}")
            
            with col4:
                avg_size = total_size_bytes / num_datasets if num_datasets > 0 else 0
                st.metric("Avg Size", f"{avg_size / (1024**2):.2f} MB")
            
            st.markdown("---")
            
            # Dataset size distribution
            st.subheader("Dataset Size Distribution")
            
            dataset_names = [row[1] for row in rows]
            dataset_sizes = [row[2] / (1024**2) for row in rows]  # Convert to MB
            
            chart_data = pd.DataFrame({
                "Dataset": dataset_names,
                "Size (MB)": dataset_sizes
            })
            
            st.bar_chart(chart_data.set_index("Dataset"))
            
            # Row count analysis
            st.subheader("Row Count by Dataset")
            
            dataset_rows = [row[3] for row in rows]
            
            chart_data2 = pd.DataFrame({
                "Dataset": dataset_names,
                "Rows": dataset_rows
            })
            
            st.line_chart(chart_data2.set_index("Dataset"))
        
        else:
            st.info("📊 No data to analyze yet. Upload datasets first!")
    
    except Exception as e:
        st.error(f"Error loading analysis: {e}")

db.close()