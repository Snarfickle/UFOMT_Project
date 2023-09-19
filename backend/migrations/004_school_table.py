steps = [
    [
        """
        BEGIN;
        CREATE TABLE School (
            school_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone BIGINT NOT NULL,
            street VARCHAR(100),
            city VARCHAR(100),
            state VARCHAR(100),
            zip VARCHAR(15),
            student_body_count BIGINT,
            title_one_status BOOLEAN,
            district_id INT REFERENCES District(district_id),
            type_id INT REFERENCES SchoolType(type_id),
            genre_id INT REFERENCES SchoolGenre(genre_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        COMMIT;
        """,
        """
        DROP TABLE School;
        """,

    ],
]
 