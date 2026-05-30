# AEGIS — AI Incident Intelligence Dashboard

Analyze simulated service logs to detect anomalies, group incidents, score severity, and suggest fixes from a knowledge base.

## Tech Stack

- Python 3.10+
- Streamlit
- Rule-based anomaly detection + JSON knowledge base

## Quick Start

```bash
git clone https://github.com/push-main/AEGIS.git
cd AEGIS
pip install -r requirements.txt
streamlit run app.py
```

## Demo Flow

```
Logs → Detect anomaly → Group incident → Assign severity → Suggest fix
```

## Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit dashboard UI |
| `main.py` | Anomaly detection, grouping, severity, recommendations |
| `log_generator.py` | Simulated log stream with injected anomalies |
| `knowledge_base.json` | Known error patterns and resolutions |

## Features

- Time-based anomaly detection (error spikes per minute)
- Incident grouping with cross-log correlation hints
- Severity scoring (LOW / MEDIUM / HIGH)
- Knowledge-base-driven fix suggestions

## Limitations & Future Work

- Uses simulated logs, not live ingestion
- Detection is threshold-based, not ML-driven
- Knowledge base is static JSON (could expand to a searchable store)

