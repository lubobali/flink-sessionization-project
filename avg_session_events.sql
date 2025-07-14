-- avg_session_events.sql

SELECT
    host,
    AVG(event_count) AS avg_events_per_session
FROM (
    SELECT
        session_id,
        host,
        COUNT(*) AS event_count
    FROM sessionized_events
    GROUP BY session_id, host
) AS session_counts
WHERE host IN ('zachwilson.techcreator.io', 'zachwilson.tech', 'lulu.techcreator.io')
GROUP BY host
ORDER BY host;
