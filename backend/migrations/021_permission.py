steps = [[
    """
    CREATE TABLE permission (
        permission_id SERIAL PRIMARY KEY,
        type_id INTEGER REFERENCES UserType(type_id),
        resource_id INTEGER REFERENCES Resource(resource_id),
        action_id INTEGER REFERENCES Action(action_id),
        can_access BOOLEAN NOT NULL
    );
    """,
    """"
    DROP TABLE permission;
    """,
]]
