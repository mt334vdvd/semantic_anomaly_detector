import sqlite3
import streamlit as st
import pandas as pd

DB_FILE = "auction.db"

# ---------- DB CONNECTION ----------
def get_connection():
    return sqlite3.connect(DB_FILE)

# ---------- FETCH DATA ----------
def get_items():
    conn = get_connection()
    query = """
    SELECT i.item_id, i.title, i.description, a.status,
           COUNT(b.bid_id) AS total_bids
    FROM Item i
    JOIN Auction a ON i.item_id = a.item_id
    LEFT JOIN Bid b ON i.item_id = b.item_id
    GROUP BY i.item_id, a.status;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def place_bid(item_id, bidder_id, bid_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Bid (item_id, bidder_id, bid_amount, bid_time) VALUES (?, ?, ?, datetime('now'))",
        (item_id, bidder_id, bid_amount),
    )
    conn.commit()
    conn.close()

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Auction System", page_icon="🎯", layout="centered")

st.title("🎯 Online Auction System")

items = get_items()

for _, row in items.iterrows():
    with st.container():
        st.subheader(row["title"])
        st.write(row["description"])
        st.write(f"**Status:** {row['status']}")
        st.write(f"**Total Bids:** {row['total_bids']}")

        if row["status"] == "active":
            bidder_id = st.text_input(f"Enter User ID for {row['title']}", key=f"user_{row['item_id']}")
            bid_amount = st.number_input(f"Enter Bid Amount for {row['title']}", min_value=1.0, step=1.0, key=f"bid_{row['item_id']}")
            if st.button(f"Place Bid on {row['title']}", key=f"btn_{row['item_id']}"):
                if bidder_id.strip():
                    place_bid(row["item_id"], bidder_id, bid_amount)
                    st.success(f"✅ Bid of {bid_amount} placed by User {bidder_id} on {row['title']}")
                else:
                    st.error("⚠️ Please enter a valid User ID")
        else:
            st.info("⛔ Auction Closed")

    st.divider()
