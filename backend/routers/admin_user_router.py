from fastapi import APIRouter, Depends, HTTPException, Request
from queries.app_user_query import AppUserIn, AppUserOut, AppUserRepo
# from authenticator import authenticator
import bcrypt
from auth_utils.auth_utils import requires_permission, get_current_user
from .app_user_router import hash_password


router = APIRouter()


@router.post("/api/admin-users", response_model=AppUserOut)
@requires_permission("create", "app-user")
def create_admin_user (
        request: Request,
        user: AppUserIn,
        repo: AppUserRepo = Depends(AppUserRepo),
        get_current_user: AppUserIn = Depends(get_current_user)
):
    user.password = hash_password(user.password)
    user.username = user.username.lower()

    result = repo.create_app_user(user)
        
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
