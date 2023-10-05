from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from queries.app_user_query import AppUserRepo, AppUserIn
from functools import wraps
from typing import Optional
# JWT Configurations
SECRET_KEY = "your_super_secret_key"  # TODO: Use a secure random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Pydantic models for token handling
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to encode the user data into a JWT token
def token_encoder(user_id: int):
    to_encode = {"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "user_id": user_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode the JWT token and get user data
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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


# Dependency to get the current user from the token
async def get_current_user(
        token: Optional[str] = Depends(oauth2_scheme)) -> Optional[AppUserIn]:

    repo = AppUserRepo()

    if not token:
        return None  # Return None if no token is provided
    try:
        # Decoding the JWT token to get the user_id.
        user_id = decode_token(token)
        # Fetch the user details from the database using the decoded user_id.
        user = repo.get_app_user(user_id) 
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token raisins!")
    except Exception as e:
        raise e

def requires_permission(action: str, resource: str):

    async def check_permission(request: Request):
        token = request.headers.get("Authorization")
        
        if token is None or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token is missing")
        token_str = token.split(" ")[1]
        current_user = await get_current_user(token_str)
        if current_user is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        repo = AppUserRepo()
        has_permission = repo.check_permission_query(current_user.type_id, action, resource)
        print("check_permission: ",has_permission)
        print("current user: ",current_user.type_id,"action: ", action,"resource: ", resource)

        if not has_permission:
            raise HTTPException(status_code=401, detail="Access Forbidden: Insufficient Permissions")
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
