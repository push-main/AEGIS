from log_generator import generate_logs
from collections import Counter
from collections import defaultdict
import json

def load_knowledge_base():
    with open("knowledge_base.json", "r") as f:
        return json.load(f)

knowledge_base = load_knowledge_base()

def detect_anomalies(logs):
    time_buckets = defaultdict(list)

   
    for log in logs:
        minute = log["timestamp"].replace(second=0, microsecond=0)
        time_buckets[minute].append(log)

    anomalies = []

    for minute, messages in time_buckets.items():
        error_count = sum(1 for log in messages if "ERROR" in log["message"])

        if error_count > 5:  
            anomalies.append({
                "time": minute,
                "error_count": error_count,
                "messages": [log["message"] for log in messages],
                "logs": messages
            })

    return anomalies

def correlate_logs(anomaly):
    messages = anomaly["messages"]

    has_db_error = any("Database timeout" in msg for msg in messages)
    has_memory_issue = any("memory" in msg.lower() for msg in messages)
    has_cpu_issue = any("cpu" in msg.lower() for msg in messages)

    if has_db_error and has_memory_issue:
        return "Memory pressure may be affecting database performance"

    if has_db_error and has_cpu_issue:
        return "High CPU usage may be causing database delays"

    return None

def group_incidents(anomalies):
    incidents = []
    for anomaly in anomalies:
        error_logs = [msg for msg in anomaly["messages"] if "ERROR" in msg]
        correlation = correlate_logs(anomaly)
        if error_logs:
            most_common_error = max(set(error_logs), key=error_logs.count)

            services = [log["service"] for log in anomaly.get("logs", [])] if "logs" in anomaly else []
            service = services[0] if services else "Unknown"

            incident = {
                "type": most_common_error,
                "count": anomaly["error_count"],
                "time": anomaly["time"],
                "service": service,
                "correlation": correlation
            }

            incidents.append(incident)

    return incidents


def calculate_severity(incident):
    count = incident["count"]
    

    error_rate = count / 60  

    if error_rate > 0.15:   
        return "HIGH"
    elif error_rate > 0.05: 
        return "MEDIUM"
    else:
        return "LOW"


def suggest_resolution(incident):
    incident_error = incident["type"].lower()
    incident_service = incident.get("service", "").lower()

    best_match = None

    for entry in knowledge_base:
        kb_error = entry["error"].lower()
        kb_service = entry["service"].lower()

        if kb_error in incident_error and kb_service in incident_service:
            best_match = entry
            break

    if best_match:
        return {
            "resolution": best_match["resolution"],
            "cause": best_match["cause"]
        }
    else:
        return {
            "resolution": "No known fix — investigate logs manually",
            "cause": "Unknown issue"
        }


def main():
    logs = generate_logs()

    print("\n--- GENERATED LOGS ---")
    for log in logs[:20]:
        print(log)

    anomalies = detect_anomalies(logs)
    incidents = group_incidents(anomalies)

    print("\n--- DETECTED INCIDENTS ---")

    for incident in incidents:
        severity = calculate_severity(incident)
        result = suggest_resolution(incident)


        print("\n🕒 Time:", incident["time"])
        print("🚨 Incident:", incident["type"])
        print("📊 Count:", incident["count"])
        print("🔥 Severity:", severity)
        print("Possible Cause:", result["cause"])
        print("Suggested Fix:", result["resolution"])


if __name__ == "__main__":
    main()