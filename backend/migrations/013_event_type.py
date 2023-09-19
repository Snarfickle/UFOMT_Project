steps = [[
    """
    BEGIN;
    CREATE TABLE event_type (
        event_type_id SERIAL PRIMARY KEY,
        name VARCHAR(200),
        description TEXT
    );
    INSERT INTO event_type (name, description) VALUES
    ('C. OBC Performances', 'Performances organized by OBC.'),
    ('B. OBC Classroom Implementation', 'Classroom sessions led by OBC for implementation strategies.'),
    ('A. OBC Workshops', 'Hands-on workshops organized by OBC.'),
    ('A. Student/Teacher in Attendance', 'Regular attendance tracking for students and teachers.'),
    ('A. UHSMTA Adjudication/Feedback', 'Feedback and review sessions for UHSMTA participants.'),
    ('B. UHSMTA Group/1-on-1 Coaching', 'Coaching sessions provided by UHSMTA in both group and individual settings.'),
    ('C. UHSMTA Workshops', 'Skill development workshops organized by UHSMTA.'),
    ('D. UHSMTA Awards Show', 'Annual awards ceremony hosted by UHSMTA.'),
    ('E. UHSMTA Winners', 'Recognition event for top-performing UHSMTA participants.'),
    ('F. UHSMTA INTERNS', 'Internship program under the UHSMTA initiative.'),
    ('G. UHSMTA LES MISERABLES', 'Special event or performance related to "Les Misérables" under the UHSMTA banner.');
    
    COMMIT;
    """,
    """
    DROP TABLE event_type;
    """,
 ]]
