from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.app_user_type_query import UserTypeIn, UserTypeOut, UserTypeRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/usertypes", response_model=UserTypeOut)
def create_user_type(
    user_type: UserTypeIn,
    repo: UserTypeRepo = Depends(UserTypeRepo)
):
    result = repo.create_user_type(user_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a UserType by its ID
@router.get("/usertypes/{type_id}", response_model=UserTypeOut)
def read_user_type(
    type_id: int,
    repo: UserTypeRepo = Depends(UserTypeRepo)
):
    result = repo.get_user_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a UserType by its ID
@router.put("/usertypes/{type_id}", response_model=UserTypeOut)
def update_user_type(
    type_id: int,
    user_type: UserTypeIn,
    repo: UserTypeRepo = Depends(UserTypeRepo)
):
    result = repo.update_user_type(type_id, user_type)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a UserType by its ID
@router.delete("/usertypes/{type_id}", response_model=dict)
def delete_user_type(
    type_id: int,
    repo: UserTypeRepo = Depends(UserTypeRepo)
):
    result = repo.delete_user_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all UserTypes
@router.get("/usertypes", response_model=List[UserTypeOut])
def list_user_types(
    repo: UserTypeRepo = Depends(UserTypeRepo)
):
    return repo.list_user_types()
