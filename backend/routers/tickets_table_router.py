from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.tickets_table_query import TicketIn, TicketOut, TicketRepo
# from authenticator import authenticator

router = APIRouter()

# Endpoint to create a new Ticket
@router.post("/tickets", response_model=TicketOut)
def create_ticket(
    ticket: TicketIn,
    repo: TicketRepo = Depends(TicketRepo)
):
    result = repo.create_ticket(ticket)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Ticket by its ID
@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def read_ticket(
    ticket_id: int,
    repo: TicketRepo = Depends(TicketRepo)
):
    result = repo.get_ticket(ticket_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Ticket by its ID
@router.put("/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    ticket: TicketIn,
    repo: TicketRepo = Depends(TicketRepo)
):
    result = repo.update_ticket(ticket_id, ticket)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Ticket by its ID
@router.delete("/tickets/{ticket_id}", response_model=dict)
def delete_ticket(
    ticket_id: int,
    repo: TicketRepo = Depends(TicketRepo)
):
    result = repo.delete_ticket(ticket_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Tickets
@router.get("/tickets", response_model=List[TicketOut])
def list_tickets(
    repo: TicketRepo = Depends(TicketRepo)
):
    return repo.list_tickets()
