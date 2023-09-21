from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.event_date_table_query import EventDateIn, EventDateOut, EventDateRepo
# from authenticator import authenticator

router = APIRouter()

# Endpoint to create a new EventDate
@router.post("/event-dates", response_model=EventDateOut)
def create_event_date(
    event_date: EventDateIn,
    repo: EventDateRepo = Depends(EventDateRepo)
):
    result = repo.create_event_date(event_date)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventDate by its ID
@router.get("/event-dates/{date_id}", response_model=EventDateOut)
def read_event_date(
    date_id: int,
    repo: EventDateRepo = Depends(EventDateRepo)
):
    result = repo.get_event_date(date_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventDate by its ID
@router.put("/event-dates/{date_id}", response_model=EventDateOut)
def update_event_date(
    date_id: int,
    event_date: EventDateIn,
    repo: EventDateRepo = Depends(EventDateRepo)
):
    result = repo.update_event_date(date_id, event_date)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventDate by its ID
@router.delete("/event-dates/{date_id}", response_model=dict)
def delete_event_date(
    date_id: int,
    repo: EventDateRepo = Depends(EventDateRepo)
):
    result = repo.delete_event_date(date_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventDates
@router.get("/event-dates", response_model=List[EventDateOut])
def list_event_dates(
    repo: EventDateRepo = Depends(EventDateRepo)
):
    return repo.list_event_dates()
