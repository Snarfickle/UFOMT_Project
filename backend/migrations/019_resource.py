steps = [[
    """
    BEGIN;
    CREATE TABLE resource(
        resource_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    ); 
    COMMIT;
    """,
    """
    DROP TABLE resource;
    """,
]]
