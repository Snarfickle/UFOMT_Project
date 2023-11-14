from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from queries.app_user_query import AppUserRepo, AppUserIn
from functools import wraps
from typing import Optional
import os
# JWT Configurations

SECRET_KEY = os.getenv("SIGNING_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Pydantic models for token handling
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to encode the user data into a JWT token
def token_encoder(user_id: int):
    access_token_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_payload = {"exp": access_token_expire, "user_id": user_id}
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    refresh_token_expire = datetime.utcnow() + timedelta(days=7)  # Or any suitable duration
    refresh_payload = {"exp": refresh_token_expire, "user_id": user_id}
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


# Function to decode the JWT token and get user data
def decode_token(token: str, token_type: str = "access"):
    try:
        if token_type == "access":
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        elif token_type == "refresh":
            # Different validation rules can be applied for refresh tokens if needed
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        else:
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id: int = payload.get("user_id")
        if user_id is None:
            raise TypeError(message="user_id is None")
        return user_id
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token - DecodeError")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")



# Dependency to get the current user from the http-only cookie
async def get_current_user(request: Request) -> Optional[AppUserIn]:
    repo = AppUserRepo()

    access_token = request.cookies.get("access_token")
    if not access_token:
        return None

    try:
        user_id = decode_token(access_token)
        user = repo.get_app_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise e

# Update the requires_permission decorator to use the cookie
def requires_permission(action: str, resource: str):
    async def check_permission(request: Request):
        current_user = await get_current_user(request)
        if current_user is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        repo = AppUserRepo()
        has_permission = repo.check_permission_query(current_user.type_id, action, resource)

        if not has_permission:
            raise HTTPException(status_code=403, detail="Access Forbidden: Insufficient Permissions")
        return current_user

    def decorator(route_function):
        @wraps(route_function)
        async def secure_route(*args, **kwargs):
            request = kwargs.get("request")
            await check_permission(request)
            result = route_function(*args, **kwargs)
            return result
        return secure_route
    
    return decorator
