from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.events_program_table_query import EventsProgramIn, EventsProgramOut, EventsProgramRepo
# from authenticator import authenticator

router = APIRouter()

# Endpoint to create a new EventsProgram
@router.post("/events-programs", response_model=EventsProgramOut)
def create_events_program(
    events_program: EventsProgramIn,
    repo: EventsProgramRepo = Depends(EventsProgramRepo)
):
    result = repo.create_events_program(events_program)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventsProgram by its ID
@router.get("/events-programs/{event_id}", response_model=EventsProgramOut)
def read_events_program(
    event_id: int,
    repo: EventsProgramRepo = Depends(EventsProgramRepo)
):
    result = repo.get_events_program(event_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventsProgram by its ID
@router.put("/events-programs/{event_id}", response_model=EventsProgramOut)
def update_events_program(
    event_id: int,
    events_program: EventsProgramIn,
    repo: EventsProgramRepo = Depends(EventsProgramRepo)
):
    result = repo.update_events_program(event_id, events_program)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventsProgram by its ID
@router.delete("/events-programs/{event_id}", response_model=dict)
def delete_events_program(
    event_id: int,
    repo: EventsProgramRepo = Depends(EventsProgramRepo)
):
    result = repo.delete_events_program(event_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventsPrograms
@router.get("/events-programs", response_model=List[EventsProgramOut])
def list_events_programs(
    repo: EventsProgramRepo = Depends(EventsProgramRepo)
):
    return repo.list_events_programs()
