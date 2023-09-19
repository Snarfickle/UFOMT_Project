steps = [[
    """
    BEGIN;
    CREATE TABLE grades (
    grade_id SERIAL PRIMARY KEY,
    grade VARCHAR(100),
    description TEXT
    );

   INSERT INTO grades (grade, description) VALUES
    ('Grade 1', 'Elementary'),
    ('Grade 2', 'Elementary'),
    ('Grade 3', 'Elementary'),
    ('Grade 4', 'Elementary'),
    ('Grade 5', 'Elementary'),
    ('Grade 6', 'Middle School'),
    ('Grade 7', 'Middle School'),
    ('Grade 8', 'Middle School'),
    ('Grade 9', 'High School'),
    ('Grade 10', 'High School'),
    ('Grade 11', 'High School'),
    ('Grade 12', 'High School'),
    ('College', 'Post-secondary education, often leading to a degree.'),
    ('Community', 'Enthusiasts and lifelong learners engaged in educational pursuits outside the traditional grade structure.');

    COMMIT;
    """,
    """
    DROP TABLE grades;
    """,
]]
