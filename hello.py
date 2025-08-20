import sqlite3

# Connect to database (creates auction.db if it doesn't exist)
conn = sqlite3.connect("auction.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Auction (
    auction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    status TEXT CHECK(status IN ('Active', 'Closed')) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Bid (
    bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    user_id INTEGER,
    amount REAL NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(item_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);
""")

# Insert sample data
cursor.execute("INSERT INTO User (username, email) VALUES ('Alice', 'alice@example.com');")
cursor.execute("INSERT INTO User (username, email) VALUES ('Bob', 'bob@example.com');")

cursor.execute("INSERT INTO Item (title, description) VALUES ('Laptop', 'Gaming laptop with RTX 4060');")
cursor.execute("INSERT INTO Item (title, description) VALUES ('Phone', 'Latest smartphone, 128GB');")

cursor.execute("INSERT INTO Auction (item_id, status) VALUES (1, 'Active');")
cursor.execute("INSERT INTO Auction (item_id, status) VALUES (2, 'Closed');")

cursor.execute("INSERT INTO Bid (item_id, user_id, amount) VALUES (1, 1, 600.0);")
cursor.execute("INSERT INTO Bid (item_id, user_id, amount) VALUES (1, 2, 650.0);")

# Save changes and close
conn.commit()
conn.close()

print("✅ Database created successfully with sample data.")
