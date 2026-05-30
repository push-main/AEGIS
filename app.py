import streamlit as st
from log_generator import generate_logs
from main import detect_anomalies, group_incidents, calculate_severity, suggest_resolution

st.set_page_config(page_title="AEGIS Dashboard", layout="wide")

st.title("🚀 AEGIS — AI Incident Intelligence Dashboard")

if "logs" not in st.session_state or st.button("🔄 Generate New Logs"):
    st.session_state.logs = generate_logs()

logs = st.session_state.logs

anomalies = detect_anomalies(logs)
incidents = group_incidents(anomalies)


st.subheader("📜 Recent Logs")

log_text = "\n".join([
    f"{log['timestamp']} [{log['service']}] - {log['message']}"
    for log in logs[:30]
])

st.text_area("Logs", log_text, height=250)


st.subheader("🚨 Detected Incidents")

if any(calculate_severity(inc) == "HIGH" for inc in incidents):
    st.error("🚨 Critical incident detected — immediate action required")
elif incidents:
    st.warning("⚠️ Potential issues detected")
else:
    st.success("✅ System operating normally")


if incidents:
    for i, incident in enumerate(incidents):
        severity = calculate_severity(incident)
        result = suggest_resolution(incident)

        with st.container():
            st.markdown(f"## 🚨 Incident {i+1}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"🕒 **Time:** {incident['time']}")
                st.write(f"🧩 **Service:** {incident.get('service', 'Unknown')}")
                st.write(f"📌 **Type:** {incident['type']}")

            with col2:
                st.write(f"📊 **Count:** {incident['count']}")

                if severity == "HIGH":
                    st.error(f"🔥 Severity: {severity}")
                elif severity == "MEDIUM":
                    st.warning(f"⚠️ Severity: {severity}")
                else:
                    st.info(f"ℹ️ Severity: {severity}")

            st.markdown("### 🧠 Analysis")
            st.write(f"**Possible Cause:** {result['cause']}")

            if incident.get("correlation"):
                st.info(f"🔍 Insight: {incident['correlation']}")

            st.success(f"🛠 Suggested Fix: {result['resolution']}")

            st.divider()


st.subheader("📊 System Summary")

total_logs = len(logs)
total_incidents = len(incidents)

col1, col2 = st.columns(2)

col1.metric("Total Logs Processed", total_logs)
col2.metric("Incidents Detected", total_incidents)

if total_incidents == 0:
    st.success("No anomalies detected — system stable")
else:
    st.warning("System requires attention")

st.info("System uses time-based anomaly detection and knowledge-driven incident analysis.")