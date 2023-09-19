steps = [[
    """
    BEGIN;
    CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES event_dates(event_id),
    event_date_id INTEGER REFERENCES event_dates(event_date_id),
    ticket_price INTEGER REFERENCES event_dates(ticket_price),
    )
    COMMIT;
    """,
    """
    DROP TABLE tickets;
    """,
]]
