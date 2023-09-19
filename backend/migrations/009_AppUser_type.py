steps = [
    [
    """
    BEGIN;
    CREATE TABLE UserType (
        type_id SERIAL PRIMARY KEY,
        type VARCHAR(100) UNIQUE NOT NULL,
        description TEXT
    );

    INSERT INTO UserType (type, description) VALUES
    ('teacher', 'Teacher type user'),
    ('student', 'Student type user'),
    ('OBC', 'OBC type user'),
    ('staff', 'Staff type user'),
    ('administration', 'Administration type user');
    
    COMMIT;
    """, 

    """
    DROP TABLE UserType;
    """,
    ],
]
