from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

# Input model for events_programs
class EventsProgramIn(BaseModel):
    event_template_id: int
    name: str
    description: str
    location_id: int
    coordinator_id: int
    event_type_id: int

# Output model for events_programs
class EventsProgramOut(EventsProgramIn):
    event_id: int

class EventsProgramRepo:
    def create_events_program(self, events_program: EventsProgramIn) -> Union[EventsProgramOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO events_programs (event_template_id, name, description, location_id, coordinator_id, event_type_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *;
                    """,
                    [events_program.event_template_id, events_program.name, events_program.description, events_program.location_id, events_program.coordinator_id, events_program.event_type_id]
                )
                record = db.fetchone()
                return EventsProgramOut(**record)
    
    def get_events_program(self, event_id: int) -> Union[EventsProgramOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM events_programs
                    WHERE event_id = %s;
                    """,
                    [event_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No events_program found with this ID."}
                return EventsProgramOut(**record)
    
    def update_events_program(self, event_id: int, events_program: EventsProgramIn) -> Union[EventsProgramOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE events_programs
                    SET event_template_id = %s,
                        name = %s,
                        description = %s,
                        location_id = %s,
                        coordinator_id = %s,
                        event_type_id = %s
                    WHERE event_id = %s
                    RETURNING *;
                    """,
                    [events_program.event_template_id, events_program.name, events_program.description, events_program.location_id, events_program.coordinator_id, events_program.event_type_id, event_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No events_program found with this ID."}
                return EventsProgramOut(**record)
    
    def delete_events_program(self, event_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM events_programs
                    WHERE event_id = %s
                    RETURNING *;
                    """,
                    [event_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No events_program found with this ID."}
                return {"message": "events_program deleted successfully"}
    
    def list_events_programs(self) -> List[EventsProgramOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM events_programs;
                    """
                )
                records = db.fetchall()
                return [EventsProgramOut(**record) for record in records]
