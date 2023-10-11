steps = [[
    """
    BEGIN;
    
    INSERT INTO event_template (name, location_id) VALUES ('Gianni Schicchi & Buoso’s Ghost', 2);
    INSERT INTO event_template (name, location_id) VALUES ('Guys & Dolls', 2);
    INSERT INTO event_template (name, location_id) VALUES ('CATS', 2);
    INSERT INTO event_template (name, location_id) VALUES ('Anything Goes', 2);
    INSERT INTO event_template (name, location_id) VALUES ('Galaxy of Stars', 2);
    INSERT INTO event_template (name, location_id) VALUES ('Verdi’s Requiem AFC Concert', 2);
    INSERT INTO event_template (name, location_id) VALUES ('Little Shop', 1);
    INSERT INTO event_template (name, location_id) VALUES ('The Pianists', 1);
    INSERT INTO event_template (name, location_id) VALUES ('Vocal Competition Semi Finals', 1);
    INSERT INTO event_template (name, location_id) VALUES ('Vocal Competition Finals', 1);

    COMMIT;
    """,
    """
    -- No Steps
    """,
]]
