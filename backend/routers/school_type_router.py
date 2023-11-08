from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.school_type_query import SchoolTypeIn, SchoolTypeOut, SchoolTypeRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new SchoolType
@router.post("/api/schooltypes", response_model=SchoolTypeOut)
@requires_permission(action="create", resource="school-type") 
def create_school_type(
    request: Request,
    school_type: SchoolTypeIn,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_school_type(school_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to get a SchoolType by its ID
@router.get("/api/schooltypes/{type_id}", response_model=SchoolTypeOut)
@requires_permission(action="read", resource="school-type") 
def read_school_type(
    request: Request,
    type_id: int,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_school_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to get a list of SchoolTypes
@router.get("/api/schooltypes", response_model=List[SchoolTypeOut])
@requires_permission(action="list", resource="school-type") 
def list_school_type(
    request: Request,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.list_school_type()
    return result

# Endpoint to update a SchoolType by its ID
@router.put("/api/schooltypes/{type_id}", response_model=SchoolTypeOut)
@requires_permission(action="update", resource="school-type") 
def update_school_type(
    request: Request,
    type_id: int,
    school_type: SchoolTypeIn,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_school_type(type_id, school_type)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a SchoolType by its ID
@router.delete("/api/schooltypes/{type_id}", response_model=dict)
@requires_permission(action="delete", resource="school-type") 
def delete_school_type(
    request: Request,
    type_id: int,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_school_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
