from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.app_user_type_query import UserTypeIn, UserTypeOut, UserTypeRepo
from queries.app_user_query import AppUserIn
from auth_utils.auth_utils import requires_permission, get_current_user

router = APIRouter()

@router.post("/api/usertypes", response_model=UserTypeOut)
@requires_permission(action="create", resource="app-user-type")
def create_user_type(
    request: Request,
    user_type: UserTypeIn,
    repo: UserTypeRepo = Depends(UserTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_user_type(user_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a UserType by its ID
@router.get("/api/usertypes/{type_id}", response_model=UserTypeOut)
@requires_permission(action="read", resource="app-user-type")
def read_user_type(
    request: Request,
    type_id: int,
    repo: UserTypeRepo = Depends(UserTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_user_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a UserType by its ID
@router.put("/api/usertypes/{type_id}", response_model=UserTypeOut)
@requires_permission(action="update", resource="app-user-type")
def update_user_type(
    request: Request,
    type_id: int,
    user_type: UserTypeIn,
    repo: UserTypeRepo = Depends(UserTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_user_type(type_id, user_type)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a UserType by its ID
@router.delete("/api/usertypes/{type_id}", response_model=dict)
@requires_permission(action="delete", resource="app-user-type")
def delete_user_type(
    request: Request,
    type_id: int,
    repo: UserTypeRepo = Depends(UserTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_user_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all UserTypes
@router.get("/api/usertypes", response_model=List[UserTypeOut])
@requires_permission(action="list", resource="app-user-type")
def list_user_types(
    request: Request,
    repo: UserTypeRepo = Depends(UserTypeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_user_types()
