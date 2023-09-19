steps = [
    [
        """
        BEGIN;

        CREATE TABLE tickets (
            ticket_id SERIAL PRIMARY KEY,
            event_date_id INTEGER REFERENCES event_dates(event_dates_id),
            app_user_id INTEGER REFERENCES app_user(user_id),
            seat_number VARCHAR(50),
            order_number VARCHAR(50),
            ticket_pulled BOOLEAN DEFAULT FALSE,
            ticket_mailed BOOLEAN DEFAULT FALSE,
            notes TEXT,
            status_type INTEGER REFERENCES ticket_status(ticket_status_id)
        );

        COMMIT;
        """,
        """
        DROP TABLE tickets;
        """,
    ]
]
