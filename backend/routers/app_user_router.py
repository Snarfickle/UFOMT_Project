from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.app_user_query import AppUserIn, AppUserOut, AppUserRepo, AppUserPassUpdate
import bcrypt
from auth_utils.auth_utils import requires_permission, get_current_user, oauth2_scheme, decode_token

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

router = APIRouter()

# Endpoint to create a new AppUser
@router.post("/api/app-users", response_model=AppUserOut)
def create_app_user(
    user: AppUserIn,
    repo: AppUserRepo = Depends(AppUserRepo)
):
    user.password = hash_password(user.password)
    user.username = user.username.lower()
            
    if user.type_id > 2:
        print("User type is higher than student or teacher!")
        raise HTTPException(status_code=403, detail="User not authorized to create this user type")

    result = repo.create_app_user(user)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch an AppUser by its ID
@router.get("/api/app-users/id/{user_id}", response_model=AppUserOut)
@requires_permission("read", "app-user")
def read_app_user(
    request: Request,
    user_id: int,
    repo: AppUserRepo = Depends(AppUserRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_app_user(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update an AppUser by its ID
@router.put("/api/app-users/{user_id}", response_model=AppUserOut)
@requires_permission("update", "app-user")
def update_app_user(
    request: Request,
    user_id: int,
    user: AppUserIn,
    repo: AppUserRepo = Depends(AppUserRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    user.password = hash_password(user.password)
    result = repo.update_app_user(user_id, user)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete an AppUser by its ID
@router.delete("/api/app-users/{user_id}", response_model=dict)
@requires_permission("delete", "app-user")
def delete_app_user(
    request: Request,
    user_id: int,
    repo: AppUserRepo = Depends(AppUserRepo),
    current_user: AppUserIn = Depends(get_current_user)
    
):
    result = repo.delete_app_user(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all AppUsers
@router.get("/api/app-users", response_model=List[AppUserOut])
@requires_permission("list", "app-user")
def list_app_users(
    request: Request,
    repo: AppUserRepo = Depends(AppUserRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_app_users()

# Endpoint to fetch an AppUser by its ID
@router.get("/api/app-users/username/{username}", response_model=AppUserOut)
@requires_permission("read", "app-user")
def read_app_user(
    request: Request,
    username: str,
    repo: AppUserRepo = Depends(AppUserRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_user_by_username(username)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.put("/api/app-users/password/{user_id}", response_model=AppUserOut)
@requires_permission("update", "app-user")
def update_app_user(
    request: Request,
    user_id: int,
    user: AppUserPassUpdate,
    repo: AppUserRepo = Depends(AppUserRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    user.password = hash_password(user.password)
    result = repo.update_user_pass(user_id, user)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
