from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.location_query import LocationIn, LocationOut, LocationRepo
# from authenticator import authenticator

router = APIRouter()

# Endpoint to create a new Location
@router.post("/locations", response_model=LocationOut)
def create_location(
    location: LocationIn,
    repo: LocationRepo = Depends(LocationRepo)
):
    result = repo.create_location(location)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Location by its ID
@router.get("/locations/{location_id}", response_model=LocationOut)
def read_location(
    location_id: int,
    repo: LocationRepo = Depends(LocationRepo)
):
    result = repo.get_location(location_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Location by its ID
@router.put("/locations/{location_id}", response_model=LocationOut)
def update_location(
    location_id: int,
    location: LocationIn,
    repo: LocationRepo = Depends(LocationRepo)
):
    result = repo.update_location(location_id, location)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Location by its ID
@router.delete("/locations/{location_id}", response_model=dict)
def delete_location(
    location_id: int,
    repo: LocationRepo = Depends(LocationRepo)
):
    result = repo.delete_location(location_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Locations
@router.get("/locations", response_model=List[LocationOut])
def list_locations(
    repo: LocationRepo = Depends(LocationRepo)
):
    return repo.list_locations()
