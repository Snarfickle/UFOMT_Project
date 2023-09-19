steps = [[
    """
    BEGIN;
    CREATE TRIGGER update_app_user_modtime
    BEFORE UPDATE ON app_user
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();
    COMMIT;
    """,
    """
    BEGIN;
    DROP TRIGGER IF EXISTS update_app_user_modtime ON app_user;
    COMMIT;
    """,
],]
