steps = [
    [
    """
    CREATE TABLE AppUser (
        user_id SERIAL PRIMARY KEY,
        type_id INTEGER REFERENCES UserType(type_id),
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone_number BIGINT NOT NULL,
        created_date DATE DEFAULT CURRENT_DATE,
        terminated_date DATE,
        grade VARCHAR(100),
        school_id INTEGER REFERENCES School(school_id),
        cactus_id VARCHAR(100),
        active BOOLEAN,
        active_date DATE,
        notes TEXT,
        parent_guardian VARCHAR(100),
        employee_id VARCHAR(100),
        street VARCHAR(100),
        city VARCHAR(100),
        state VARCHAR(100),
        zip INTEGER
    );
    """,
    """
    DROP TABLE AppUser;
    """,
    ]
]
