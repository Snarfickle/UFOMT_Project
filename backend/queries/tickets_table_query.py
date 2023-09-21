from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

# Input model for tickets
class TicketIn(BaseModel):
    event_date_id: int
    app_user_id: int
    seat_number: str
    order_number: str
    ticket_pulled: bool
    ticket_mailed: bool
    notes: str
    status_type: int

# Output model for tickets
class TicketOut(TicketIn):
    ticket_id: int

class TicketRepo:
    def create_ticket(self, ticket: TicketIn) -> Union[TicketOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO tickets (
                        event_date_id, app_user_id, seat_number, order_number,
                        ticket_pulled, ticket_mailed, notes, status_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *;
                    """,
                    [
                        ticket.event_date_id, ticket.app_user_id, ticket.seat_number,
                        ticket.order_number, ticket.ticket_pulled, ticket.ticket_mailed,
                        ticket.notes, ticket.status_type
                    ]
                )
                record = db.fetchone()
                return TicketOut(**record)
    
    def get_ticket(self, ticket_id: int) -> Union[TicketOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM tickets
                    WHERE ticket_id = %s;
                    """,
                    [ticket_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No ticket found with this ID."}
                return TicketOut(**record)
    
    def update_ticket(self, ticket_id: int, ticket: TicketIn) -> Union[TicketOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE tickets
                    SET event_date_id = %s,
                        app_user_id = %s,
                        seat_number = %s,
                        order_number = %s,
                        ticket_pulled = %s,
                        ticket_mailed = %s,
                        notes = %s,
                        status_type = %s
                    WHERE ticket_id = %s
                    RETURNING *;
                    """,
                    [
                        ticket.event_date_id, ticket.app_user_id, ticket.seat_number,
                        ticket.order_number, ticket.ticket_pulled, ticket.ticket_mailed,
                        ticket.notes, ticket.status_type, ticket_id
                    ]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No ticket found with this ID."}
                return TicketOut(**record)
    
    def delete_ticket(self, ticket_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM tickets
                    WHERE ticket_id = %s
                    RETURNING *;
                    """,
                    [ticket_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No ticket found with this ID."}
                return {"message": "ticket deleted successfully"}
    
    def list_tickets(self) -> List[TicketOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM tickets;
                    """
                )
                records = db.fetchall()
                return [TicketOut(**record) for record in records]
