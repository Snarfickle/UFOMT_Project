steps = [[
    """
    BEGIN;
    CREATE TABLE action(
        action_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    ); 
    COMMIT;
    """,
    """
    DROP TABLE action;
    """,
]]
