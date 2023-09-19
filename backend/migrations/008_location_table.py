steps= [[
    """
    CREATE TABLE location (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(200) NOT NULL,
    state VARCHAR(200) NOT NULL,
    zip BIGINT NOT NULL,
    location_description TEXT
    );
    """,
    """
    DROP TABLE location;
    """,  
]]
