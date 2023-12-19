steps = [[
    """
    BEGIN;
    CREATE TABLE teacher_status (
    teacher_status_id SERIAL PRIMARY KEY,
    status VARCHAR(100),
    description TEXT
    );

    INSERT INTO teacher_status ( status, description) VALUES
    ('First year','Beginning the program this year and will certainly need help running the program from the mentors.'),
    ('Second year','Worked last year and might need slightly more help running the program this year from the mentors.'),
    ('Third year','Have worked at least two years and will only need the standard help from mentors in running the program.');
    COMMIT;
    """,
    """
    DROP TABLE teacher_status;
    """,
]]
