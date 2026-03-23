import random
from datetime import datetime, timedelta


def generate_logs():
    logs = []

    base_time = datetime.now()

    services = ["AuthService", "PaymentService", "DatabaseService"]

    normal_events = [
        "INFO: Service started",
        "INFO: Request processed",
        "INFO: User login successful"
    ]

    error_events = [
        ("DatabaseService", "ERROR: Database timeout"),
        ("PaymentService", "ERROR: Service unavailable"),
        ("AuthService", "WARNING: Token validation delay"),
        ("DatabaseService", "WARNING: High memory usage")
    ]

    # Normal logs
    for i in range(50):
        timestamp = base_time + timedelta(seconds=i * 5)

        if random.random() < 0.8:
            logs.append({
                "timestamp": timestamp,
                "service": random.choice(services),
                "message": random.choice(normal_events)
            })
        else:
            service, msg = random.choice(error_events)
            logs.append({
                "timestamp": timestamp,
                "service": service,
                "message": msg
            })

    # Inject anomaly (DB spike)
    anomaly_time = base_time + timedelta(minutes=5)

    for i in range(10):
        logs.append({
            "timestamp": anomaly_time + timedelta(seconds=i),
            "service": "DatabaseService",
            "message": "ERROR: Database timeout"
        })

    return logs