steps = [[
    """
    BEGIN;
    CREATE TABLE District (
        district_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        zipcode INT NOT NULL
    );
    COMMIT;
    """,
    """
    DROP TABLE District;
    """,
],]
