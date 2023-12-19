steps = [[
    """
    BEGIN;
    
    -- Little Shop at Utah Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-05', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-06', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-13', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-17', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-18', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-20', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-22', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-24', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-26', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-29', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-07-31', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (1, '2023-08-01', NULL, '19:30', '21:30');

    -- Gianni Schicchi & Buoso’s Ghost at Ellen Eccles Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (2, '2023-07-10', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (2, '2023-07-19', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (2, '2023-07-25', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (2, '2023-08-02', NULL, '19:30', '21:30');

    -- Guys & Dolls at Ellen Eccles Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (3, '2023-07-11', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (3, '2023-07-16', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (3, '2023-07-18', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (3, '2023-07-25', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (3, '2023-07-27', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (3, '2023-08-02', NULL, '13:00', '15:00');

    -- CATS at Ellen Eccles Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-12', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-12', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-13', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-15', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-17', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-19', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-24', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-27', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-07-31', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (4, '2023-08-03', NULL, '13:00', '15:00');

    -- Anything Goes at Ellen Eccles Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (5, '2023-07-12', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (5, '2023-07-20', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (5, '2023-07-22', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (5, '2023-07-26', NULL, '19:30', '21:30');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (5, '2023-08-01', NULL, '13:00', '15:00');
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (5, '2023-08-03', NULL, '19:30', '21:30');

    -- The Pianists at Utah Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (6, '2023-07-16', NULL, '13:00', '15:00');

    -- Vocal Competition Semi Finals at Utah Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (7, '2023-07-23', NULL, '13:00', '15:00');

    -- Galaxy of Stars at Ellen Eccles Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (8, '2023-07-23', NULL, '19:30', '21:30');

    -- Vocal Competition Finals at Utah Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (9, '2023-07-29', NULL, '19:30', '21:30');

    -- Verdi’s Requiem AFC Concert at Ellen Eccles Theater
    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time) VALUES (10, '2023-07-30', NULL, '19:30', '21:30');

    COMMIT;
    """,
    """
    -- No Steps
    """,
]]
