steps = [[
    """
    BEGIN;
    CREATE TABLE event_dates(
    event_dates_id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events_programs(event_id),
    date DATE,
    ticket_price INTEGER,
    start_time TIME,
    end_time TIME, 
    duration INTERVAL GENERATED ALWAYS AS (end_time - start_time) STORED
    );
    COMMIT;
    """,
    """
    DROP TABLE event_dates;
    """,
]]
