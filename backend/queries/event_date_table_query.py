from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool
from datetime import time, date, timedelta, datetime

# Input model for event_dates
class EventDateIn(BaseModel):
    event_id: int
    date: date
    ticket_price: int
    start_time: time
    end_time: time

# Output model for event_dates
class EventDateOut(EventDateIn):
    event_dates_id: int
    duration: timedelta


def timedelta_to_time(delta: timedelta) -> time:
    return (datetime.min + delta).time()


class EventDateRepo:
    def create_event_date(self, event_date: EventDateIn) -> Union[EventDateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO event_dates (event_id, date, ticket_price, start_time, end_time)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                    """,
                    [event_date.event_id, event_date.date, event_date.ticket_price, event_date.start_time, event_date.end_time]
                )
                record = db.fetchone()
                # Convert duration from timedelta to time
                # record['duration'] = (datetime.min + record['duration']).time()
                
                # # Map 'event_dates_id' to 'date_id'
                # record['date_id'] = record.pop('event_dates_id')
                
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
                        date = %s,
                        ticket_price = %s,
                        start_time = %s,
                        end_time = %s
                    WHERE date_id = %s
                    RETURNING *;
                    """,
                    [event_date.event_id, event_date.date, event_date.ticket_price, event_date.start_time, event_date.end_time, date_id]
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
