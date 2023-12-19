steps = [[
    """
    BEGIN;
    CREATE TABLE resource(
        resource_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    ); 

    INSERT INTO resource(name) VALUES

    ('app-user'),
    ('app-user-type'),
    ('classroom'),
    ('district'),
    ('event-date'),
    ('event-template'),
    ('event-type'),
    ('events-program'),
    ('grades'),
    ('location'),
    ('school-genre'),
    ('school-type'),
    ('schools'),
    ('teacher-status'),
    ('tickets-status'),
    ('tickets'),
    ('form-submission');
    
    COMMIT;
    """,
    """
    DROP TABLE resource;
    """,
]]
