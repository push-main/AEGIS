import streamlit as st
from log_generator import generate_logs
from main import detect_anomalies, group_incidents, calculate_severity, suggest_resolution

st.set_page_config(page_title="AegisOps Dashboard", layout="wide")

st.title("🚀 AegisOps - AI Incident Intelligence Dashboard")

# 🔄 Generate logs button
if st.button("🔄 Generate New Logs"):
    logs = generate_logs()
else:
    logs = generate_logs()

# Process logs
anomalies = detect_anomalies(logs)
incidents = group_incidents(anomalies)

# -----------------------
# 📜 LOGS SECTION
# -----------------------
st.subheader("📜 Recent Logs")

log_text = "\n".join([
    f"{log['timestamp']} [{log['service']}] - {log['message']}"
    for log in logs[:30]
])

st.text_area("Logs", log_text, height=250)

# -----------------------
# 🚨 INCIDENT HEADER
# -----------------------
st.subheader("🚨 Detected Incidents")

if any(calculate_severity(inc) == "HIGH" for inc in incidents):
    st.error("🚨 Critical incident detected — immediate action required")
elif incidents:
    st.warning("⚠️ Potential issues detected")
else:
    st.success("✅ System operating normally")

# -----------------------
# 🚨 INCIDENT CARDS
# -----------------------
if incidents:
    for i, incident in enumerate(incidents):
        severity = calculate_severity(incident)
        result = suggest_resolution(incident)

        with st.container():
            st.markdown(f"## 🚨 Incident {i+1}")

            col1, col2 = st.columns(2)

            # LEFT COLUMN
            with col1:
                st.write(f"🕒 **Time:** {incident['time']}")
                st.write(f"🧩 **Service:** {incident.get('service', 'Unknown')}")
                st.write(f"📌 **Type:** {incident['type']}")

            # RIGHT COLUMN
            with col2:
                st.write(f"📊 **Count:** {incident['count']}")

                if severity == "HIGH":
                    st.error(f"🔥 Severity: {severity}")
                elif severity == "MEDIUM":
                    st.warning(f"⚠️ Severity: {severity}")
                else:
                    st.info(f"ℹ️ Severity: {severity}")

            # 🧠 Analysis Section
            st.markdown("### 🧠 Analysis")
            st.write(f"**Possible Cause:** {result['cause']}")

            # 🔍 Correlation Insight (if exists)
            if incident.get("correlation"):
                st.info(f"🔍 Insight: {incident['correlation']}")

            # 🛠 Fix Highlight
            st.success(f"🛠 Suggested Fix: {result['resolution']}")

            st.divider()

# -----------------------
# 📊 SUMMARY
# -----------------------
st.subheader("📊 System Summary")

total_logs = len(logs)
total_incidents = len(incidents)

col1, col2 = st.columns(2)

col1.metric("Total Logs Processed", total_logs)
col2.metric("Incidents Detected", total_incidents)

# Status message
if total_incidents == 0:
    st.success("No anomalies detected — system stable")
else:
    st.warning("System requires attention")

st.info("System uses time-based anomaly detection and knowledge-driven incident analysis.")