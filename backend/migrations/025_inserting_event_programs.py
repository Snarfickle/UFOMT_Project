steps = [[
    """
    BEGIN;
    
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (7, 'Little Shop', 1, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (1, 'Gianni Schicchi & Buoso’s Ghost', 2, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (2, 'Guys & Dolls', 2, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (3, 'CATS', 2, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (4, 'Anything Goes', 2, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (8, 'The Pianists', 1, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (9, 'Vocal Competition Semi Finals', 1, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (5, 'Galaxy of Stars', 2, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (10, 'Vocal Competition Finals', 1, 1, 4);
    INSERT INTO events_programs (event_template_id, name, location_id, coordinator_id, event_type_id) VALUES (6, 'Verdi’s Requiem AFC Concert', 2, 1, 4);
    
    COMMIT;
    """,
    """
    -- No Steps
    """,
]]
