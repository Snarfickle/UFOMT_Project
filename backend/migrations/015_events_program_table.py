steps = [[
    """
    BEGIN;
    CREATE TABLE events_programs (
    event_id SERIAL PRIMARY KEY,
    event_template_id INTEGER REFERENCES event_template(template_id),
    name VARCHAR(200),
    description TEXT,
    location_id INTEGER REFERENCES location(location_id),
    coordinator_id INTEGER REFERENCES app_user(user_id),
    event_type_id INTEGER REFERENCES event_type(event_type_id)
    );
    COMMIT;
    """,
    """
    DROP TABLE events_programs;
    """,
]]
