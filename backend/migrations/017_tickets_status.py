steps = [[
    """
    BEGIN;
    CREATE TABLE ticket_status (
    ticket_status_id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    description TEXT
    );

    INSERT INTO ticket_status (name, description) VALUES
    ('incorrect info', 'The information provided with the ticket is incorrect.'),
    ('in will-call', 'The ticket is waiting for pickup at the will-call window.'),
    ('calling us back', 'The ticket holder mentioned they would call back.'),
    ('called and left a message', 'A call was made and a message was left for the ticket holder.'),
    ('left a message try calling again later', 'A message was left; a follow-up call is needed.'),
    ('currently being worked*', 'The ticket issue or query is currently being addressed.'),
    ('No show', 'The ticket holder did not show up for the event.');
    COMMIT;
    """,
    """
    DROP TABLE ticket_status;
    """,
]]
