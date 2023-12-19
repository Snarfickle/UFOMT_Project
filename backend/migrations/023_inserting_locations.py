steps = [[
    """
    BEGIN;
    
    INSERT INTO location (name, address, city, state, zip, seat_number) VALUES ('Utah Theater', '18 W Center Street', 'Logan', 'UT', 84321, 0);
    INSERT INTO location (name, address, city, state, zip, seat_number) VALUES ('Ellen Eccles Theater', '43 S Main St', 'Logan', 'UT', 84321, 0);
    
    COMMIT;
    """,
    """
    -- No Steps
    """,
]]
