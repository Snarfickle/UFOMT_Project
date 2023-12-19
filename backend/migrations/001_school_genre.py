steps = [
    [
        """
        BEGIN;
        CREATE TABLE SchoolGenre (
            genre_id SERIAL PRIMARY KEY,
            type VARCHAR(100) UNIQUE NOT NULL,
            description TEXT
        );

        INSERT INTO SchoolGenre (type, description) VALUES
        ('Elementary', 'grades 1-4'),
        ('Middle school', 'grades 5-8'),
        ('Jr. High', 'grades 7-8'),
        ('High School', 'grades 9-12'),
        ('College', 'Any year of college'),
        ('Other', 'Educational institutions or stages not specifically categorized above, including pre-school, vocational training, adult education, etc.');

        COMMIT;
        """,

        """
        DROP TABLE SchoolGenre;
        """,
    ],
]
