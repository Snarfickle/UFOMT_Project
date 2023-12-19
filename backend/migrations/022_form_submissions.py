steps = [[
    """
    BEGIN;
    CREATE TABLE FormSubmissions (
    submission_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(100) NOT NULL,
    grade_id INTEGER REFERENCES grades(grade_id),
    teacher_status BOOLEAN NOT NULL,
    cactus_number VARCHAR(100),
    guardian_name VARCHAR(100),
    classroom_size INTEGER,
    number_of_classrooms INTEGER,
    event_program_id INTEGER REFERENCES events_programs(event_id),
    event_date_id INTEGER REFERENCES event_dates(event_dates_id) NOT NULL,
    ticket_id INTEGER REFERENCES tickets(ticket_id),
    school_id INTEGER REFERENCES School(school_id),
    school_type_id INTEGER REFERENCES SchoolType(type_id),
    school_genre_id INTEGER REFERENCES SchoolGenre(genre_id)
);

    COMMIT;
    """,
    """
    DROP TABLE FormSubmissions;
    """,
]]
