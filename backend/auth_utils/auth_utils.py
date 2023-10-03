from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from queries.app_user_query import AppUserRepo, AppUserIn

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
            raise credentials_exception
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# OAuth2PasswordBearer instance for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), repo: AppUserRepo = Depends(AppUserRepo)) -> AppUserIn:
    """
    Decode the JWT token and retrieve the user details.
    """
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
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise
