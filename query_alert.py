import sqlite3

conn = sqlite3.connect("shared/alerts.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 5;")
for row in cursor.fetchall():
    print(row)
conn.close()