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
WHERE host IN ('site-a.example.com', 'site-b.example.com', 'site-c.example.com')
GROUP BY host
ORDER BY host;
