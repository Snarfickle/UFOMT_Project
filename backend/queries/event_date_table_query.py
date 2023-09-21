from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool
from datetime import datetime

# Input model for event_dates
class EventDateIn(BaseModel):
    event_id: int
    start_date: datetime
    end_date: datetime

# Output model for event_dates
class EventDateOut(EventDateIn):
    date_id: int

class EventDateRepo:
    def create_event_date(self, event_date: EventDateIn) -> Union[EventDateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO event_dates (event_id, start_date, end_date)
                    VALUES (%s, %s, %s)
                    RETURNING *;
                    """,
                    [event_date.event_id, event_date.start_date, event_date.end_date]
                )
                record = db.fetchone()
                return EventDateOut(**record)
    
    def get_event_date(self, date_id: int) -> Union[EventDateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM event_dates
                    WHERE date_id = %s;
                    """,
                    [date_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_date found with this ID."}
                return EventDateOut(**record)
    
    def update_event_date(self, date_id: int, event_date: EventDateIn) -> Union[EventDateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE event_dates
                    SET event_id = %s,
                        start_date = %s,
                        end_date = %s
                    WHERE date_id = %s
                    RETURNING *;
                    """,
                    [event_date.event_id, event_date.start_date, event_date.end_date, date_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_date found with this ID."}
                return EventDateOut(**record)
    
    def delete_event_date(self, date_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM event_dates
                    WHERE date_id = %s
                    RETURNING *;
                    """,
                    [date_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_date found with this ID."}
                return {"message": "event_date deleted successfully"}
    
    def list_event_dates(self) -> List[EventDateOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM event_dates;
                    """
                )
                records = db.fetchall()
                return [EventDateOut(**record) for record in records]
