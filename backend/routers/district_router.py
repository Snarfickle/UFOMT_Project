from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.district_query import DistrictIn, DistrictOut, DistrictRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/districts", response_model=DistrictOut)
def create_district(
    district: DistrictIn,
    repo: DistrictRepo = Depends(DistrictRepo)
):
    result = repo.create_district(district)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a District by its ID
@router.get("/districts/{district_id}", response_model=DistrictOut)
def read_district(
    district_id: int,
    repo: DistrictRepo = Depends(DistrictRepo)
):
    result = repo.get_district(district_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a District by its ID
@router.put("/districts/{district_id}", response_model=DistrictOut)
def update_district(
    district_id: int,
    district: DistrictIn,
    repo: DistrictRepo = Depends(DistrictRepo)
):
    result = repo.update_district(district_id, district)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a District by its ID
@router.delete("/districts/{district_id}", response_model=dict)
def delete_district(
    district_id: int,
    repo: DistrictRepo = Depends(DistrictRepo)
):
    result = repo.delete_district(district_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Districts
@router.get("/districts", response_model=List[DistrictOut])
def list_districts(
    repo: DistrictRepo = Depends(DistrictRepo)
):
    return repo.list_districts()
