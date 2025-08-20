import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hi",
    database="plane"
)

cursor = conn.cursor()