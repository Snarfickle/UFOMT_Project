from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.schools_query import Error, SchoolIn, SchoolOut, SchoolRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/schools", response_model=SchoolOut)
def create_school(
    school: SchoolIn,
    repo: SchoolRepo = Depends(SchoolRepo),
    # account_data: Dict =  Depends(authenticator.get_current_account_data),
):
    result = repo.create_school(school)
    print(school)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/schools/{school_id}", response_model=SchoolOut)
def read_school(
    school_id: int,
    repo: SchoolRepo = Depends(SchoolRepo)  # Assuming SchoolRepo is imported from the appropriate module
):
    result = repo.get_school(school_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a school by its ID
@router.put("/schools/{school_id}", response_model=SchoolOut)
def update_school(
    school_id: int,
    school: SchoolIn,
    repo: SchoolRepo = Depends(SchoolRepo)
):
    result = repo.update_school(school_id, school)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a school by its ID
@router.delete("/schools/{school_id}", response_model=dict)
def delete_school(
    school_id: int,
    repo: SchoolRepo = Depends(SchoolRepo)
):
    result = repo.delete_school(school_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all schools (optional)
@router.get("/schools", response_model=List[SchoolOut])
def list_schools(
    repo: SchoolRepo = Depends(SchoolRepo)
):
    result = repo.get_all_schools()
    return result
