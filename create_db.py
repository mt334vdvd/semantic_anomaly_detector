import sqlite3

conn = sqlite3.connect("auction.db")
c = conn.cursor()

# Drop old tables if they exist
c.executescript("""
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Auction;
DROP TABLE IF EXISTS Bid;
""")

# Create tables
c.executescript("""
CREATE TABLE Users (
  user_id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100)
);

CREATE TABLE Item (
  item_id INT PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  seller_id INT,
  FOREIGN KEY (seller_id) REFERENCES Users(user_id)
);

CREATE TABLE Auction (
  auction_id INT PRIMARY KEY,
  item_id INT,
  start_time DATETIME,
  end_time DATETIME,
  status VARCHAR(20),
  FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

CREATE TABLE Bid (
  bid_id INT PRIMARY KEY,
  item_id INT,
  bidder_id INT,
  bid_amount DECIMAL(10,2),
  bid_time DATETIME,
  FOREIGN KEY (item_id) REFERENCES Item(item_id),
  FOREIGN KEY (bidder_id) REFERENCES Users(user_id)
);
""")

# Insert sample data
c.executescript("""
INSERT INTO Users (user_id, name, email) VALUES
(1, 'Mahi', 'mahi@example.com'),
(2, 'Aarav', 'aarav@example.com'),
(3, 'Kiara', 'kiara@example.com');

INSERT INTO Item (item_id, title, description, seller_id) VALUES
(101, 'Vintage Camera', 'Old-school film camera from the 80s', 1),
(102, 'Gaming Laptop', 'High-performance laptop for gaming', 2);

INSERT INTO Auction (auction_id, item_id, start_time, end_time, status) VALUES
(201, 101, '2025-08-18 10:00:00', '2025-08-20 10:00:00', 'active'),
(202, 102, '2025-08-17 09:00:00', '2025-08-19 09:00:00', 'closed');

INSERT INTO Bid (bid_id, item_id, bidder_id, bid_amount, bid_time) VALUES
(301, 101, 2, 1500.00, '2025-08-18 11:00:00'),
(302, 101, 3, 1600.00, '2025-08-18 12:30:00'),
(303, 102, 1, 75000.00, '2025-08-17 10:15:00');
""")

conn.commit()
conn.close()
print("✅ auction.db created with sample data")
