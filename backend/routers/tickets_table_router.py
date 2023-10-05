from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.tickets_table_query import TicketIn, TicketOut, TicketRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new Ticket
@router.post("/tickets", response_model=TicketOut)
@requires_permission(action="create", resource="tickets")
def create_ticket(
    request: Request,
    ticket: TicketIn,
    repo: TicketRepo = Depends(TicketRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_ticket(ticket)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Ticket by its ID
@router.get("/tickets/{ticket_id}", response_model=TicketOut)
@requires_permission(action="create", resource="tickets")
def read_ticket(
    request: Request,
    ticket_id: int,
    repo: TicketRepo = Depends(TicketRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_ticket(ticket_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Ticket by its ID
@router.put("/tickets/{ticket_id}", response_model=TicketOut)
@requires_permission(action="create", resource="tickets")
def update_ticket(
    request: Request,
    ticket_id: int,
    ticket: TicketIn,
    repo: TicketRepo = Depends(TicketRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_ticket(ticket_id, ticket)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Ticket by its ID
@router.delete("/tickets/{ticket_id}", response_model=dict)
@requires_permission(action="create", resource="tickets")
def delete_ticket(
    request: Request,
    ticket_id: int,
    repo: TicketRepo = Depends(TicketRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_ticket(ticket_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Tickets
@router.get("/tickets", response_model=List[TicketOut])
@requires_permission(action="create", resource="tickets")
def list_tickets(
    request: Request,
    repo: TicketRepo = Depends(TicketRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_tickets()
