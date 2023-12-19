from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

class EventTypeIn(BaseModel):
    name: str
    description: str

# Output model for event_type
class EventTypeOut(EventTypeIn):
    event_type_id: int

class EventTypeRepo:
    def create_event_type(self, event_type: EventTypeIn) -> Union[EventTypeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO event_type (name, description)
                    VALUES (%s, %s)
                    RETURNING *;
                    """,
                    [event_type.name, event_type.description]
                )
                record = db.fetchone()
                return EventTypeOut(**record)
    
    def get_event_type(self, event_type_id: int) -> Union[EventTypeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM event_type
                    WHERE event_type_id = %s;
                    """,
                    [event_type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_type found with this ID."}
                return EventTypeOut(**record)
    
    def update_event_type(self, event_type_id: int, event_type: EventTypeIn) -> Union[EventTypeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE event_type
                    SET name = %s,
                        description = %s
                    WHERE event_type_id = %s
                    RETURNING *;
                    """,
                    [event_type.name, event_type.description, event_type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_type found with this ID."}
                return EventTypeOut(**record)
    
    def delete_event_type(self, event_type_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM event_type
                    WHERE event_type_id = %s
                    RETURNING *;
                    """,
                    [event_type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_type found with this ID."}
                return {"message": "event_type deleted successfully"}
    
    def list_event_types(self) -> List[EventTypeOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM event_type;
                    """
                )
                records = db.fetchall()
                return [EventTypeOut(**record) for record in records]
