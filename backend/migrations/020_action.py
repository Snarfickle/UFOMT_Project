steps = [[
    """
    BEGIN;
    CREATE TABLE action(
        action_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    ); 

    INSERT INTO action(name) VALUES
    ('create'),
    ('read'),
    ('update'),
    ('delete'),
    ('list');
    
    COMMIT;
    """,
    """
    DROP TABLE action;
    """,
]]
