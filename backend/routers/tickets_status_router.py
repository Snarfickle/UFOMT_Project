from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.tickets_status_query import TicketStatusIn, TicketStatusOut, TicketStatusRepo
# from authenticator import authenticator

router = APIRouter()

# Endpoint to create a new TicketStatus
@router.post("/ticket-statuses", response_model=TicketStatusOut)
def create_ticket_status(
    ticket_status: TicketStatusIn,
    repo: TicketStatusRepo = Depends(TicketStatusRepo)
):
    result = repo.create_ticket_status(ticket_status)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a TicketStatus by its ID
@router.get("/ticket-statuses/{ticket_status_id}", response_model=TicketStatusOut)
def read_ticket_status(
    ticket_status_id: int,
    repo: TicketStatusRepo = Depends(TicketStatusRepo)
):
    result = repo.get_ticket_status(ticket_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a TicketStatus by its ID
@router.put("/ticket-statuses/{ticket_status_id}", response_model=TicketStatusOut)
def update_ticket_status(
    ticket_status_id: int,
    ticket_status: TicketStatusIn,
    repo: TicketStatusRepo = Depends(TicketStatusRepo)
):
    result = repo.update_ticket_status(ticket_status_id, ticket_status)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a TicketStatus by its ID
@router.delete("/ticket-statuses/{ticket_status_id}", response_model=dict)
def delete_ticket_status(
    ticket_status_id: int,
    repo: TicketStatusRepo = Depends(TicketStatusRepo)
):
    result = repo.delete_ticket_status(ticket_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all TicketStatuses
@router.get("/ticket-statuses", response_model=List[TicketStatusOut])
def list_ticket_statuses(
    repo: TicketStatusRepo = Depends(TicketStatusRepo)
):
    return repo.list_ticket_statuses()
