# Flink Sessionization Project

This project demonstrates a real-time data processing pipeline using Apache Flink, Kafka, and PostgreSQL.

It implements sessionization on web events, enriching data with geolocation and writing results to both a database and Kafka.

## Features

- 🧠 Apache Flink + PyFlink for event-time processing
- 🗃️ Kafka source and sink integration
- 🧪 PostgreSQL output for analysis
- 🌍 Geolocation UDF (`get_location`)
- 📦 Dockerized environment with `docker-compose`

## Files Included

- `start_job.py` – Main Flink job
- `get_location.py` – UDF for IP enrichment
- `docker-compose.yml` – Full pipeline stack
- `Dockerfile` – Custom Flink image with Python
- `requirements.txt` – Python dependencies
- `Makefile` – Shortcut to send events and run job

## How to Run

```bash
docker compose up --build -d
make send-event

