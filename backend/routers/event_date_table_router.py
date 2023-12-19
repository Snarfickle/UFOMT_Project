from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.event_date_table_query import EventDateIn, EventDateOut, EventDateRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new EventDate
@router.post("/api/event-dates", response_model=EventDateOut)
@requires_permission(action="create", resource="event-date")  
def create_event_date(
    request: Request,
    event_date: EventDateIn,
    repo: EventDateRepo = Depends(EventDateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_event_date(event_date)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventDate by its ID
@router.get("/api/event-dates/{date_id}", response_model=EventDateOut)
@requires_permission(action="read", resource="event-date")  
def read_event_date(
    request: Request,
    date_id: int,
    repo: EventDateRepo = Depends(EventDateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_event_date(date_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventDate by its ID
@router.put("/api/event-dates/{date_id}", response_model=EventDateOut)
@requires_permission(action="update", resource="event-date")  
def update_event_date(
    request: Request,
    date_id: int,
    event_date: EventDateIn,
    repo: EventDateRepo = Depends(EventDateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_event_date(date_id, event_date)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventDate by its ID
@router.delete("/api/event-dates/{date_id}", response_model=dict)
@requires_permission(action="delete", resource="event-date")  
def delete_event_date(
    request: Request,
    date_id: int,
    repo: EventDateRepo = Depends(EventDateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_event_date(date_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventDates
@router.get("/api/event-dates", response_model=List[EventDateOut])
# @requires_permission(action="list", resource="event-date")  
def list_event_dates(
    request: Request,
    repo: EventDateRepo = Depends(EventDateRepo),
    # current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_event_dates()
