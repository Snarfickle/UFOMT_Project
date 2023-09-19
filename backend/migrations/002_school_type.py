steps = [
    [
        """
        BEGIN;

        CREATE TABLE SchoolType (
            type_id SERIAL PRIMARY KEY,
            type VARCHAR(100) UNIQUE NOT NULL,
            description TEXT
        );

        INSERT INTO SchoolType (type, description) VALUES
        ('Public', 'Publicly funded institutions overseen by local or state education agencies. They are established by the state and open to all students within their jurisdiction.'),
        ('Charter', 'Publicly funded schools that operate independently under a specific charter or contract with an authorizing body, offering more flexibility in curriculum and operations compared to traditional public schools.'),
        ('Private', 'Institutions funded through tuition, private grants, and donations rather than public tax dollars. They operate independently of state education agencies and often have selective admission policies.'),
        ('Home school', 'An educational option where parents or guardians take on the primary responsibility of educating their children outside of traditional school settings, typically within the home environment.'),
        ('Community', 'Educational environments or initiatives that may not fit traditional categories but play a role in community-based learning, often emphasizing collaborative and localized education.' );

        COMMIT;
        """,
        """
        DROP TABLE SchoolType;
        """,
    ],
]
