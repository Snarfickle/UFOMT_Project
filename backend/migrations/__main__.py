async def migrate():
    from . import down, up, LATEST, ZERO
    import os
    import sys

    db_url = os.environ["DATABASE_URL"]

    if len(sys.argv) < 2:
        print("Command: up|down [amount]")
        exit(1)
    direction = sys.argv[1]
    amount = sys.argv[2] if len(sys.argv) > 2 else None
    if direction == "up":
        if amount is None:
            amount = LATEST
        else:
            try:
                amount = int(amount)
            except ValueError:
                print(f"Unknown amount {amount}")
        await up(db_url, to=amount)
    elif direction == "down":
        if amount is None:
            amount = 1
        elif amount == "zero":
            amount = ZERO
        else:
            try:
                amount = int(amount)
            except ValueError:
                print(f"Unknown amount {amount}")
        await down(db_url, to=amount)


if __name__ == "__main__":
    from asyncio import run

    # from psycopg_pool import ConnectionPool
    # import os

    # try:
    #     pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])
    #     with pool.connection() as conn:
    #         with conn.cursor() as db:
    #             db.execute(
    #                 """
    #                 DROP TABLE messages;
    #                 DROP TRIGGER IF EXISTS writer_check ON resources;
    #                 DROP FUNCTION IF EXISTS check_writer_is_therapist;
    #                 DROP TABLE resources;
    #                 DROP TRIGGER IF EXISTS appointee_check ON appointments;
    #                 DROP FUNCTION IF EXISTS check_therapist_id_is_therapist;
    #                 DROP TABLE appointments;
    #                 DROP TABLE journals;
    #                 DROP TYPE mood;
    #                 DROP TABLE jotters;
    #                 DROP TYPE user_type;
    #                 DELETE FROM migrations;
    #                 """,
    #             )
    # except Exception as e:
    #     print("Error while deleting database")
    #     print(e)
    run(migrate())
    print("Migrations have run.")
