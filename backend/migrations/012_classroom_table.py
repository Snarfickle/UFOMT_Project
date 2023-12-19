steps = [[
    """
    BEGIN;
    CREATE TABLE classroom (
    classroom_id SERIAL PRIMARY KEY,
    size INTEGER,
    grade_id INTEGER REFERENCES grades (grade_id),
    teacher_id INTEGER REFERENCES app_user (user_id),
    drama_mentor_id INTEGER REFERENCES app_user (user_id),
    art_mentor_id INTEGER REFERENCES app_user (user_id),
    music_mentor_id INTEGER REFERENCES app_user (user_id)
    );
    COMMIT;
    """,
    """
    DROP TABLE classroom;
    """,
]]
