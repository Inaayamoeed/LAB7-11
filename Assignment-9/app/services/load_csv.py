import pandas as pd
from app.data.db import connect_database
 #loading Cyer Incidents 
def load_cyber_incidents(csv_path="DATA/cyber_incidents.csv"):
    df = pd.read_csv(csv_path)
    conn = connect_database()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO cyber_incidents (title, severity, status, date)
            VALUES (?, ?, ?, ?)
        """, (row["title"], row["severity"], row["status"], row["date"]))

    conn.commit()
    conn.close()
    print("Cyber incidents loaded")

#loading Datasets Metadata 
def load_datasets_metadata(csv_path="DATA/datasets_metadata.csv"):
    df = pd.read_csv(csv_path)
    conn = connect_database()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO datasets_metadata (name, source, category, size)
            VALUES (?, ?, ?, ?)
        """, (row["name"], row["source"], row["category"], row["size"]))

    conn.commit()
    conn.close()
    print("Datasets metadata loaded")

#loading IT Tickets
def load_it_tickets(csv_path="DATA/it_tickets.csv"):
    df = pd.read_csv(csv_path)
    conn = connect_database()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO it_tickets (title, priority, status, created_date)
            VALUES (?, ?, ?, ?)
        """, (row["title"], row["priority"], row["status"], row["created_date"]))

    conn.commit()
    conn.close()
    print("IT tickets loaded")