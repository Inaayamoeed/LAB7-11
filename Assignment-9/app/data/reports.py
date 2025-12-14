from app.data.db import connect_database

#all cyber incidents
def get_all_cyber_incidents():
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, severity, status, date FROM cyber_incidents")
    rows = cursor.fetchall()

    conn.close()
    return rows

# 2) High severity or critical incidents
def get_high_severity_incidents():
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, severity, status, date
        FROM cyber_incidents
        WHERE severity IN ('high', 'critical')
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows

# 3) Open IT tickets only
def get_open_it_tickets():
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, priority, status, created_date
        FROM it_tickets
        WHERE status = 'open'
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows

# 4) Large datasets that are > than (min_size of 2000)
def get_large_datasets(min_size=2000):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, source, category, size
        FROM datasets_metadata
        WHERE size > ?
    """, (min_size,))
    rows = cursor.fetchall()

    conn.close()
    return rows
