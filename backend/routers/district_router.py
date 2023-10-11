from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.district_query import DistrictIn, DistrictOut, DistrictRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

@router.post("/districts", response_model=DistrictOut)
@requires_permission(action="create", resource="district")  
def create_district(
    request: Request,
    district: DistrictIn,
    repo: DistrictRepo = Depends(DistrictRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_district(district)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a District by its ID
@router.get("/districts/{district_id}", response_model=DistrictOut)
@requires_permission(action="read", resource="district")  
def read_district(
    request: Request,
    district_id: int,
    repo: DistrictRepo = Depends(DistrictRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_district(district_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a District by its ID
@router.put("/districts/{district_id}", response_model=DistrictOut)
@requires_permission(action="update", resource="district")  
def update_district(
    request: Request,
    district_id: int,
    district: DistrictIn,
    repo: DistrictRepo = Depends(DistrictRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_district(district_id, district)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a District by its ID
@router.delete("/districts/{district_id}", response_model=dict)
@requires_permission(action="delete", resource="district")  
def delete_district(
    request: Request,
    district_id: int,
    repo: DistrictRepo = Depends(DistrictRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_district(district_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Districts
@router.get("/districts", response_model=List[DistrictOut])
# @requires_permission(action="list", resource="district")  
def list_districts(
    request: Request,
    repo: DistrictRepo = Depends(DistrictRepo),
    # current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_districts()
