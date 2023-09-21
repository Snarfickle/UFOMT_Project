from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.event_type_query import EventTypeIn, EventTypeOut, EventTypeRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/event-types", response_model=EventTypeOut)
def create_event_type(
    event_type: EventTypeIn,
    repo: EventTypeRepo = Depends(EventTypeRepo)
):
    result = repo.create_event_type(event_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventType by its ID
@router.get("/event-types/{event_type_id}", response_model=EventTypeOut)
def read_event_type(
    event_type_id: int,
    repo: EventTypeRepo = Depends(EventTypeRepo)
):
    result = repo.get_event_type(event_type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventType by its ID
@router.put("/event-types/{event_type_id}", response_model=EventTypeOut)
def update_event_type(
    event_type_id: int,
    event_type: EventTypeIn,
    repo: EventTypeRepo = Depends(EventTypeRepo)
):
    result = repo.update_event_type(event_type_id, event_type)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventType by its ID
@router.delete("/event-types/{event_type_id}", response_model=dict)
def delete_event_type(
    event_type_id: int,
    repo: EventTypeRepo = Depends(EventTypeRepo)
):
    result = repo.delete_event_type(event_type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventTypes
@router.get("/event-types", response_model=List[EventTypeOut])
def list_event_types(
    repo: EventTypeRepo = Depends(EventTypeRepo)
):
    return repo.list_event_types()
