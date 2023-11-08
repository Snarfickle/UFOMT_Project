from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.event_type_query import EventTypeIn, EventTypeOut, EventTypeRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

@router.post("/api/event-types", response_model=EventTypeOut)
@requires_permission(action="create", resource="event-type") 
def create_event_type(
    request: Request,
    event_type: EventTypeIn,
    repo: EventTypeRepo = Depends(EventTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_event_type(event_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventType by its ID
@router.get("/api/event-types/{event_type_id}", response_model=EventTypeOut)
@requires_permission(action="read", resource="event-type") 
def read_event_type(
    request: Request,
    event_type_id: int,
    repo: EventTypeRepo = Depends(EventTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_event_type(event_type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventType by its ID
@router.put("/api/event-types/{event_type_id}", response_model=EventTypeOut)
@requires_permission(action="update", resource="event-type") 
def update_event_type(
    request: Request,
    event_type_id: int,
    event_type: EventTypeIn,
    repo: EventTypeRepo = Depends(EventTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_event_type(event_type_id, event_type)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventType by its ID
@router.delete("/api/event-types/{event_type_id}", response_model=dict)
@requires_permission(action="delete", resource="event-type") 
def delete_event_type(
    request: Request,
    event_type_id: int,
    repo: EventTypeRepo = Depends(EventTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_event_type(event_type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventTypes
@router.get("/api/event-types", response_model=List[EventTypeOut])
@requires_permission(action="list", resource="event-type") 
def list_event_types(
    request: Request,
    repo: EventTypeRepo = Depends(EventTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_event_types()
