steps = [[
    """
    BEGIN;
    CREATE TABLE event_template (
    template_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location_id INTEGER REFERENCES location (location_id),
    description TEXT
    );
    COMMIT;
    """,
    """
    DROP TABLE event_template;
    """,
]]
