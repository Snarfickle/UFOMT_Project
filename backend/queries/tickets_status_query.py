from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool


# Input model for ticket_status
class TicketStatusIn(BaseModel):
    name: str
    description: str

# Output model for ticket_status
class TicketStatusOut(TicketStatusIn):
    ticket_status_id: int

class TicketStatusRepo:
    def create_ticket_status(self, ticket_status: TicketStatusIn) -> Union[TicketStatusOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO ticket_status (name, description)
                    VALUES (%s, %s)
                    RETURNING *;
                    """,
                    [ticket_status.name, ticket_status.description]
                )
                record = db.fetchone()
                return TicketStatusOut(**record)
    
    def get_ticket_status(self, ticket_status_id: int) -> Union[TicketStatusOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM ticket_status
                    WHERE ticket_status_id = %s;
                    """,
                    [ticket_status_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No ticket_status found with this ID."}
                return TicketStatusOut(**record)
    
    def update_ticket_status(self, ticket_status_id: int, ticket_status: TicketStatusIn) -> Union[TicketStatusOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE ticket_status
                    SET name = %s,
                        description = %s
                    WHERE ticket_status_id = %s
                    RETURNING *;
                    """,
                    [ticket_status.name, ticket_status.description, ticket_status_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No ticket_status found with this ID."}
                return TicketStatusOut(**record)
    
    def delete_ticket_status(self, ticket_status_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM ticket_status
                    WHERE ticket_status_id = %s
                    RETURNING *;
                    """,
                    [ticket_status_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No ticket_status found with this ID."}
                return {"message": "ticket_status deleted successfully"}
    
    def list_ticket_statuses(self) -> List[TicketStatusOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM ticket_status;
                    """
                )
                records = db.fetchall()
                return [TicketStatusOut(**record) for record in records]
