# semantic_monitor.py
import os
import openai

class SemanticMonitor:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def explain(self, metric: str, value: float, proc: str, ts: int) -> str:
        if not openai.api_key:
            return "No API key set. Cannot fetch explanation."

        prompt = (
            f"At timestamp {ts}, process '{proc}' "
            f"triggered a {metric} spike of {value:.1f}%. "
            "Is this a contextually meaningful (semantic) anomaly or expected behavior? "
            "Explain in simple terms."
        )

        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a system monitoring expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=120
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"Error fetching explanation: {e}"