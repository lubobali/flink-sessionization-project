# Kafka Producer Scripts — Purpose and Usage

## Overview

This document consolidates the role and usage of the Kafka producer scripts used for testing the Flink sessionization job. Properly understanding and using these scripts ensures reliable test data generation and validation of streaming workflows.

## Scripts Included

- **send_event.py**  
  A Python script that produces web event messages to the Kafka topic `web-events`. It simulates real user events by sending JSON-formatted records with fields such as `ip`, `host`, `event_time`, and others.

- **send_test_event.py**  
  A simplified test producer that sends a single or a few controlled events to Kafka. Useful for quick connectivity tests or debugging specific scenarios.

## Role in Testing

The Kafka producers serve as the data input source for the Flink streaming job. They generate the event stream that Flink processes to sessionize user activity by IP and host.

Testing the Flink job requires valid and timely event data; these scripts help:

- Verify Kafka connectivity and topic configuration  
- Provide sample events to trigger Flink processing  
- Enable controlled testing scenarios for debugging and verification  

## Recommended Usage

1. Use `send_test_event.py` for initial tests to confirm Kafka is reachable and accepting messages.  
2. Use `send_event.py` for more realistic load testing, simulating typical user traffic patterns.  
3. Modify or extend these scripts as needed to create diverse event patterns for thorough testing.

## Execution

Run the producer scripts from the command line as follows:

```bash
python send_event.py
# or
python send_test_event.py

