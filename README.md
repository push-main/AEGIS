# AegisOps - AI Incident Intelligence Dashboard

## Overview
A system that analyzes logs to detect anomalies, identify incidents, and recommend fixes.

## Run
pip install streamlit  
streamlit run app.py

## Project Structure
- app.py → Streamlit UI
- main.py → Core logic (detection, grouping, scoring)
- log_generator.py → Simulated logs
- knowledge_base.json → Historical fixes

## Demo Flow
Logs → Detect anomaly → Group incident → Assign severity → Suggest fix

## Features
- Time-based anomaly detection
- Incident grouping
- Severity scoring
- Knowledge-based recommendations
