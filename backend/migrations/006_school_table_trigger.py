steps = [[
        """
        BEGIN;
        CREATE OR REPLACE FUNCTION update_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER update_school_modtime
        BEFORE UPDATE ON School
        FOR EACH ROW
        EXECUTE FUNCTION update_timestamp();
        COMMIT;
            
        """,
        """
        BEGIN;

        DROP TRIGGER IF EXISTS update_school_modtime ON School;
        DROP FUNCTION IF EXISTS update_timestamp();

        COMMIT;
        """,
],]
