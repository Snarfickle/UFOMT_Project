from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.location_query import LocationIn, LocationOut, LocationRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new Location
@router.post("/api/locations", response_model=LocationOut)
@requires_permission(action="create", resource="location")  
def create_location(
    request: Request,
    location: LocationIn,
    repo: LocationRepo = Depends(LocationRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_location(location)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Location by its ID
@router.get("/api/locations/{location_id}", response_model=LocationOut)
@requires_permission(action="read", resource="location")  
def read_location(
    request: Request,
    location_id: int,
    repo: LocationRepo = Depends(LocationRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_location(location_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Location by its ID
@router.put("/api/locations/{location_id}", response_model=LocationOut)
@requires_permission(action="update", resource="location")  
def update_location(
    request: Request,
    location_id: int,
    location: LocationIn,
    repo: LocationRepo = Depends(LocationRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_location(location_id, location)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Location by its ID
@router.delete("/api/locations/{location_id}", response_model=dict)
@requires_permission(action="delete", resource="location")  
def delete_location(
    request: Request,
    location_id: int,
    repo: LocationRepo = Depends(LocationRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_location(location_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Locations
@router.get("/api/locations", response_model=List[LocationOut])
@requires_permission(action="list", resource="location")  
def list_locations(
    request: Request,
    repo: LocationRepo = Depends(LocationRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_locations()
