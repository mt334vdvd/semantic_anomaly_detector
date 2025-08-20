# analytics.py
import json, sqlite3, time, statistics, psutil
from semantic_monitor import SemanticMonitor

DB_PATH = "shared/alerts.db"
METRICS_PATH = "shared/metrics.json"
WINDOW = []
WIN_SIZE = 12
SM = SemanticMonitor()

# Initialize SQLite DB
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute("""
CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY,
  timestamp INTEGER,
  metric TEXT,
  value REAL,
  process TEXT,
  explanation TEXT
)
""")
conn.commit()

def load_latest_metrics():
    try:
        with open(METRICS_PATH) as f:
            history = json.load(f)
        return history[-1] if isinstance(history, list) and history else {}
    except Exception:
        return {}

def get_top_process():
    try:
        top = max(psutil.process_iter(['name', 'cpu_percent']),
                  key=lambda p: p.info['cpu_percent'])
        return top.info['name']
    except Exception:
        return "Unknown"

def detect_and_alert():
    data = load_latest_metrics()
    ts, cpu, mem = data.get("timestamp"), data.get("cpu"), data.get("mem")

    if ts is None or cpu is None or mem is None:
        print("⚠️ Skipping: incomplete or invalid metrics")
        return

    WINDOW.append({"ts": ts, "cpu": cpu, "mem": mem})
    if len(WINDOW) > WIN_SIZE:
        WINDOW.pop(0)

    cpus = [x["cpu"] for x in WINDOW]
    mems = [x["mem"] for x in WINDOW]
    mean_cpu, sd_cpu = statistics.mean(cpus), statistics.pstdev(cpus)
    mean_mem, sd_mem = statistics.mean(mems), statistics.pstdev(mems)

    alerts = []
    if sd_cpu > 0 and abs(cpu - mean_cpu) / sd_cpu > 2.5:
        alerts.append(("cpu", cpu))
    if sd_mem > 0 and abs(mem - mean_mem) / sd_mem > 2.5:
        alerts.append(("mem", mem))

    top_proc = get_top_process()

    for metric, val in alerts:
        explanation = SM.explain(metric, val, top_proc, ts)
        conn.execute(
            "INSERT INTO alerts (timestamp, metric, value, process, explanation) VALUES (?,?,?,?,?)",
            (ts, metric, val, top_proc, explanation)
        )
        print(f"🔔 {metric.upper()} spike → {val:.1f}% | {top_proc}\n🧠 {explanation}\n")

    conn.commit()

if __name__ == "__main__":
    while True:
        try:
            detect_and_alert()
        except Exception as e:
            print("⚠️ Error:", e)
        time.sleep(5)