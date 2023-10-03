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
    ('Teacher', 'Teachers are able to create and read for schools, districts, classrooms. Event_dates, event_programs are read only'),
    ('Student', 'Students are able to create and read for schools, districts, classrooms. Event_dates, event_programs are read only'),
    ('OBC', 'Opera By Children Staff (OBC) able to create, read, list, and update for schools, districts, classrooms, event_dates, event_programs'),
    ('Staff', 'Front office staff are able to create, read, update, and list for tickets'),
    ('Administration', 'Administration are able to use all permissions for all tables');
    
    COMMIT;
    """, 

    """
    DROP TABLE UserType;
    """,
    ],
]
