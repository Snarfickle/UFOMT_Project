steps = [
    [
    """
    BEGIN;
    CREATE TABLE app_user (
        -- Below is for each user to have
        user_id SERIAL PRIMARY KEY,
        type_id INTEGER REFERENCES UserType(type_id),
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password TEXT NOT NULL,
        username VARCHAR(200) UNIQUE NOT NULL,
        phone_number BIGINT NOT NULL,
        created_date DATE DEFAULT CURRENT_DATE,
        terminated_date DATE,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        -- Below is for the teacher profile
        grade_id INTEGER REFERENCES grades(grade_id),
        school_id INTEGER REFERENCES School(school_id),
        cactus_id VARCHAR(100),
        active BOOLEAN,
        notes TEXT,
        teacher_status_id INTEGER REFERENCES teacher_status(teacher_status_id),

        -- Below is for the Student profile
        parent_guardian VARCHAR(100),

        -- Below is for the employee profile
        employee_id VARCHAR(100),
        street VARCHAR(100),
        city VARCHAR(100),
        state VARCHAR(100),
        zip INTEGER
    );
    COMMIT;
    """,
    """
    DROP TABLE app_user;
    """,
    ]
]
