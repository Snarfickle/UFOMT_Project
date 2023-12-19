from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.tickets_status_query import TicketStatusIn, TicketStatusOut, TicketStatusRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new TicketStatus
@router.post("/ticket-statuses", response_model=TicketStatusOut)
@requires_permission(action="create", resource="tickets-status")
def create_ticket_status(
    request: Request,
    ticket_status: TicketStatusIn,
    repo: TicketStatusRepo = Depends(TicketStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
    
):
    result = repo.create_ticket_status(ticket_status)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a TicketStatus by its ID
@router.get("/ticket-statuses/{ticket_status_id}", response_model=TicketStatusOut)
@requires_permission(action="read", resource="tickets-status")
def read_ticket_status(
    request: Request,
    ticket_status_id: int,
    repo: TicketStatusRepo = Depends(TicketStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_ticket_status(ticket_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a TicketStatus by its ID
@router.put("/ticket-statuses/{ticket_status_id}", response_model=TicketStatusOut)
@requires_permission(action="update", resource="tickets-status")
def update_ticket_status(
    request: Request,
    ticket_status_id: int,
    ticket_status: TicketStatusIn,
    repo: TicketStatusRepo = Depends(TicketStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_ticket_status(ticket_status_id, ticket_status)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a TicketStatus by its ID
@router.delete("/ticket-statuses/{ticket_status_id}", response_model=dict)
@requires_permission(action="delete", resource="tickets-status")
def delete_ticket_status(
    request: Request,
    ticket_status_id: int,
    repo: TicketStatusRepo = Depends(TicketStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_ticket_status(ticket_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all TicketStatuses
@router.get("/ticket-statuses", response_model=List[TicketStatusOut])
@requires_permission("list", "tickets-status")
def list_ticket_statuses(
    request: Request,
    repo: TicketStatusRepo = Depends(TicketStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_ticket_statuses()
