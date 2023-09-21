from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

class EventTemplateIn(BaseModel):
    name: str
    location_id: int
    description: str

# Output model for event_template
class EventTemplateOut(EventTemplateIn):
    template_id: int

class EventTemplateRepo:
    def create_event_template(self, event_template: EventTemplateIn) -> Union[EventTemplateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO event_template (name, location_id, description)
                    VALUES (%s, %s, %s)
                    RETURNING *;
                    """,
                    [event_template.name, event_template.location_id, event_template.description]
                )
                record = db.fetchone()
                return EventTemplateOut(**record)
    
    def get_event_template(self, template_id: int) -> Union[EventTemplateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM event_template
                    WHERE template_id = %s;
                    """,
                    [template_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_template found with this ID."}
                return EventTemplateOut(**record)
    
    def update_event_template(self, template_id: int, event_template: EventTemplateIn) -> Union[EventTemplateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE event_template
                    SET name = %s,
                        location_id = %s,
                        description = %s
                    WHERE template_id = %s
                    RETURNING *;
                    """,
                    [event_template.name, event_template.location_id, event_template.description, template_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_template found with this ID."}
                return EventTemplateOut(**record)
    
    def delete_event_template(self, template_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM event_template
                    WHERE template_id = %s
                    RETURNING *;
                    """,
                    [template_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No event_template found with this ID."}
                return {"message": "event_template deleted successfully"}
    
    def list_event_templates(self) -> List[EventTemplateOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM event_template;
                    """
                )
                records = db.fetchall()
                return [EventTemplateOut(**record) for record in records]
