steps = [
    [
        """
        CREATE TABLE School (
            school_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone BIGINT NOT NULL,
            street VARCHAR(100),
            city VARCHAR(100),
            state VARCHAR(100),
            zip VARCHAR(15),
            district VARCHAR(100)
        );
        """, 
        """
        DROP TABLE School;
        """,
    ],
]
