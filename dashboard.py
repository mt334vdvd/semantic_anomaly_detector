# dashboard.py
from flask import Flask, render_template, jsonify
import sqlite3, json

app = Flask(__name__, static_url_path="/static")  # Serves usage_chart.png

# Paths to local files
DB_PATH = "shared/alerts.db"
METRICS_PATH = "shared/metrics.json"

# Utility: Open DB connection with row access
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint: /metrics → Serve raw metrics as JSON
@app.route("/metrics")
def metrics():
    with open(METRICS_PATH) as f:
        return jsonify(json.load(f))

# Endpoint: /alerts → Serve 20 latest alerts from DB
@app.route("/alerts")
def alerts():
    db = get_db()
    rows = db.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 20").fetchall()
    return jsonify([dict(r) for r in rows])

# Homepage: Render HTML dashboard view
@app.route("/")
def index():
    return render_template("dashboard.html")

# Start the local server
if __name__ == "__main__":
    app.run(debug=True, port=5000)