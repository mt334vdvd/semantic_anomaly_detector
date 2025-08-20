# usage_chart.py
import json
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime

sns.set_theme(style="whitegrid")

# Load metrics from JSON
with open("shared/metrics.json") as f:
    metrics = json.load(f)

# Load alerts from SQLite
conn = sqlite3.connect("shared/alerts.db")
conn.row_factory = sqlite3.Row
alerts = [dict(r) for r in conn.execute("SELECT * FROM alerts ORDER BY timestamp ASC").fetchall()]
conn.close()

# Prepare data for plotting
times = [datetime.fromtimestamp(m["timestamp"] / 1000) for m in metrics]
cpu_vals = [m["cpu"] for m in metrics]
mem_vals = [m["mem"] for m in metrics]

plt.figure(figsize=(14, 6))
plt.plot(times, cpu_vals, label="CPU (%)", color="firebrick", linewidth=2.2)
plt.plot(times, mem_vals, label="Memory (%)", color="royalblue", linewidth=2.2)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gcf().autofmt_xdate()

# Overlay numeric spike markers (colored by metric type)
for alert in alerts:
    ts = datetime.fromtimestamp(alert["timestamp"] / 1000)
    val = alert["value"]
    color = "red" if alert["metric"] == "cpu" else "blue"
    plt.scatter(ts, val, color=color, edgecolors="black", zorder=6, s=70)
    plt.annotate(
        f"{val:.1f}",
        xy=(ts, val),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        color="black"
    )

plt.title("Visualization of CPU and Memory Usage", fontsize=15, weight="bold", pad=10)
plt.xlabel("Timestamp", fontsize=12)
plt.ylabel("Usage (%)", fontsize=12)
plt.legend(loc="upper right", fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()

# Save high-resolution chart
output_path = "static/usage_chart.png"
plt.savefig(output_path, dpi=300)
print(f" Scientific chart saved to {output_path}")
