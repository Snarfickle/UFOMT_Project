from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.app_user_query import AppUserIn, AppUserOut, AppUserRepo
# from authenticator import authenticator
import bcrypt
from auth_utils.auth_utils import get_current_user

def hash_password(plain_password: str) -> str:
    '''Hash a password for storing.'''
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

router = APIRouter()

# Endpoint to create a new AppUser
@router.post("/app-users", response_model=AppUserOut)
def create_app_user(
    user: AppUserIn,
    repo: AppUserRepo = Depends(AppUserRepo)
):
    user.password = hash_password(user.password)
    user.username = user.username.lower()

    result = repo.create_app_user(user)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch an AppUser by its ID
@router.get("/app-users/{user_id}", response_model=AppUserOut)
def read_app_user(
    user_id: int,
    repo: AppUserRepo = Depends(AppUserRepo)
):
    result = repo.get_app_user(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update an AppUser by its ID
@router.put("/app-users/{user_id}", response_model=AppUserOut)
def update_app_user(
    user_id: int,
    user: AppUserIn,
    repo: AppUserRepo = Depends(AppUserRepo)
):
    user.password = hash_password(user.password)
    result = repo.update_app_user(user_id, user)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete an AppUser by its ID
@router.delete("/app-users/{user_id}", response_model=dict)
def delete_app_user(
    user_id: int,
    repo: AppUserRepo = Depends(AppUserRepo)
):
    result = repo.delete_app_user(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all AppUsers
@router.get("/app-users", response_model=List[AppUserOut])
async def list_app_users(
    repo: AppUserRepo = Depends(AppUserRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    if current_user.type_id < 3: # need to implement a user file to help control the level of access to each user. 
        raise HTTPException(status_code=401, detail="Invalid user type")
    return repo.list_app_users()
    
