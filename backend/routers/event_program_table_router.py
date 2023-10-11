from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.events_program_table_query import EventsProgramIn, EventsProgramOut, EventsProgramRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new EventsProgram
@router.post("/events-programs", response_model=EventsProgramOut)
@requires_permission(action="create", resource="events-program") 
def create_events_program(
    request: Request,
    events_program: EventsProgramIn,
    repo: EventsProgramRepo = Depends(EventsProgramRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_events_program(events_program)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventsProgram by its ID
@router.get("/events-programs/{event_id}", response_model=EventsProgramOut)
@requires_permission(action="read", resource="events-program") 
def read_events_program(
    request: Request,
    event_id: int,
    repo: EventsProgramRepo = Depends(EventsProgramRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_events_program(event_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventsProgram by its ID
@router.put("/events-programs/{event_id}", response_model=EventsProgramOut)
@requires_permission(action="update", resource="events-program") 
def update_events_program(
    request: Request,
    event_id: int,
    events_program: EventsProgramIn,
    repo: EventsProgramRepo = Depends(EventsProgramRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_events_program(event_id, events_program)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventsProgram by its ID
@router.delete("/events-programs/{event_id}", response_model=dict)
@requires_permission(action="delete", resource="events-program") 
def delete_events_program(
    request: Request,
    event_id: int,
    repo: EventsProgramRepo = Depends(EventsProgramRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_events_program(event_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventsPrograms
@router.get("/events-programs", response_model=List[EventsProgramOut])
# @requires_permission(action="list", resource="events-program") 
def list_events_programs(
    request: Request,
    repo: EventsProgramRepo = Depends(EventsProgramRepo)
    # current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_events_programs()
