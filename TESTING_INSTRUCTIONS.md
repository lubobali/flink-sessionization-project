Testing Instructions

1. Run the Flink Job

- Make sure your Docker containers are running:
  docker compose up -d

- Submit the Flink job inside the jobmanager container:
  docker compose exec jobmanager /opt/flink/bin/flink run -py /opt/src/job/start_job.py --pyArchives /opt/src/pyflink_venv.tar.gz

This starts the sessionization job that processes Kafka events and writes sessionized results to PostgreSQL.

2. Verify the Flink Job is Running

- Open the Flink Web UI in your browser at:
  http://localhost:8081

- Monitor the job status and logs here.

3. Connect to the PostgreSQL Database

- Use a PostgreSQL client or CLI tool (psql) to connect:
  psql -h localhost -p 5434 -U postgres -d flink_db

Replace with your actual hostname, port, username, and database as needed.

4. Run the SQL Query to Check Sessionized Data

- Run the SQL script avg_session_events.sql by loading it in your SQL client or via:
  \i /path/to/avg_session_events.sql

5. Expected Results

- The output will show average web events per session grouped by host, e.g.:

  host                     | average_events_per_session
  ------------------------------------------------------
  zachwilson.techcreator.io | 4.5
  zachwilson.tech           | 3.8
  lulu.techcreator.io       | 5.2

- Verify these numbers align with your data and confirm correct sessionization by IP and host with a 5-minute gap.

