from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.schools_query import Error, SchoolIn, SchoolOut, SchoolRepo
from auth_utils import auth_utils
from queries.app_user_query import AppUserIn

router = APIRouter()

@router.post("/schools", response_model=SchoolOut)
@auth_utils.requires_permission(action="create", resource="schools")
def create_school(
    request: Request,
    school: SchoolIn,
    repo: SchoolRepo = Depends(SchoolRepo),
    current_user: AppUserIn = Depends(auth_utils.get_current_user)
):
    result = repo.create_school(school)
    print(school)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/schools/{school_id}", response_model=SchoolOut)
@auth_utils.requires_permission(action="read", resource="schools")
def read_school(
    request: Request,
    school_id: int,
    repo: SchoolRepo = Depends(SchoolRepo),
    current_user: AppUserIn = Depends(auth_utils.get_current_user)
):
    result = repo.get_school(school_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a school by its ID
@router.put("/schools/{school_id}", response_model=SchoolOut)
@auth_utils.requires_permission(action="update", resource="schools")
def update_school(
    request: Request,
    school_id: int,
    school: SchoolIn,
    repo: SchoolRepo = Depends(SchoolRepo),
    current_user: AppUserIn = Depends(auth_utils.get_current_user)
):
    result = repo.update_school(school_id, school)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a school by its ID
@router.delete("/schools/{school_id}", response_model=dict)
@auth_utils.requires_permission(action="delete", resource="schools")
def delete_school(
    request: Request,
    school_id: int,
    repo: SchoolRepo = Depends(SchoolRepo),
    current_user: AppUserIn = Depends(auth_utils.get_current_user)
):
    result = repo.delete_school(school_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all schools (optional)
@router.get("/schools", response_model=List[SchoolOut])
# @auth_utils.requires_permission("list", "schools")
def list_schools(
    # request: Request,
    repo: SchoolRepo = Depends(SchoolRepo),
    # current_user: AppUserIn = Depends(auth_utils.get_current_user)
):
    result = repo.get_all_schools()
    return result
