from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings, DataTypes
from pyflink.table.udf import udf
import socket
import time

# Register UDF
@udf(result_type=DataTypes.STRING())
def get_location(ip: str) -> str:
    if ip == "1.2.3.4":
        return "Chicago, IL"
    elif ip == "5.6.7.8":
        return "Sofia, Bulgaria"
    return "Unknown"

# Helper to wait for services
def wait_for_service(host, port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            socket.create_connection((host, port), timeout=2)
            print(f"✅ Connected to {host}:{port}")
            return
        except Exception as e:
            print(f"⏳ Waiting for {host}:{port}... {str(e)}")
            time.sleep(2)
    raise Exception(f"❌ Could not connect to {host}:{port} after {timeout} seconds")

def log_aggregation():
    print("✅ Creating Flink environments...")
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    print("⏳ Checking service availability...")
    wait_for_service("kafka", 9092)
    wait_for_service("postgres", 5432)

    print("✅ Registering UDF...")
    t_env.create_temporary_function("get_location", get_location)

    print("✅ Creating Kafka source table...")
    t_env.execute_sql("""
    CREATE TABLE web_events (
        ip STRING,
        host STRING,
        event_time STRING,
        event_timestamp AS TO_TIMESTAMP(event_time),
        WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'bootcamp-events-prod',
        'properties.bootstrap.servers' = 'kafka:9092',
        'properties.group.id' = 'web-events',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json',
        'json.ignore-parse-errors' = 'true'
    )
    """)

    print("✅ Creating Postgres sink table...")
    t_env.execute_sql("""
    CREATE TABLE sessionized_events (
        ip STRING,
        host STRING,
        window_start TIMESTAMP(3),
        window_end TIMESTAMP(3),
        event_count BIGINT,
        location STRING
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://host.docker.internal:5434/postgres',
        'table-name' = 'sessionized_events',
        'username' = 'postgres',
        'password' = 'postgres',
        'sink.buffer-flush.interval' = '2s',
        'sink.buffer-flush.max-rows' = '1'
    )
    """)

    print("🚀 Starting streaming job...")
    t_env.execute_sql("""
    INSERT INTO sessionized_events
    SELECT
        ip,
        host,
        SESSION_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
        SESSION_END(event_timestamp, INTERVAL '5' MINUTE) AS window_end,
        COUNT(*) AS event_count,
        get_location(ip) AS location
    FROM web_events
    GROUP BY
        ip,
        host,
        SESSION(event_timestamp, INTERVAL '5' MINUTE)
    """)

if __name__ == "__main__":
    print("🔥 start_job.py is executing")
    log_aggregation()
    print("✅ log_aggregation() submitted (you won't see this unless job finishes)")
