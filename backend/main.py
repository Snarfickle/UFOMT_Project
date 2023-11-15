from fastapi import FastAPI, Depends, HTTPException, Form, Cookie, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    schools_router,
    school_type_router,
    school_genre_router,
    district_router,
    grades_router,
    teacher_status_router,
    location_router,
    app_user_type_router,
    app_user_router,
    classroom_table_router,
    event_type_router,
    event_template_router,
    event_program_table_router,
    event_date_table_router,
    tickets_status_router,
    tickets_table_router,
    admin_user_router,
    form_submission_router,
    school_file_loader,
)
from auth_utils.auth_utils import token_encoder, Token
from queries.app_user_query import AppUserRepo
import bcrypt
import jwt
import os
from fastapi import FastAPI, Depends, HTTPException, Form, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from auth_utils.auth_utils import token_encoder, decode_token
from queries.app_user_query import AppUserRepo
import os

SECRET_KEY = os.getenv("SIGNING_KEY")
ALGORITHM = "HS256"


app = FastAPI()

origins = [
    # os.getenv("FRONTEND_URL", "default_value_if_not_set"),  # It's safer to have a default or check if it's None
    "https://ufomt-load-1431517948.us-east-1.elb.amazonaws.com",
    "http://localhost:3000",
    "https://ufomtstaff.org",
]

# print("Allowed origins for CORS:", origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
class ForwardedProtoMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            headers = dict(scope["headers"])
            if b"x-forwarded-proto" in headers:
                scheme = headers[b"x-forwarded-proto"].decode()
                scope["scheme"] = scheme
        await self.app(scope, receive, send)

# Usage
app.add_middleware(ForwardedProtoMiddleware)

@app.on_event("startup")
async def startup_event():
    try:
        from start_file import create_initial_user

        # Your script logic here
        create_initial_user()
    except ImportError as e:
        print(f"The start_file module could not be imported: {e}. Be sure to rebase or rebuild the database with a new startfile and user information.")

def hash_password(plain_password: str) -> str:
    # '''Hash a password for storing.'''
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # '''Check hashed password. Using bcrypt, the salt is saved into the hash itself.'''
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Login Endpoint
@app.post("/api/login/")
def login_for_access_token(
    response: Response, 
    username: str = Form(...), 
    password: str = Form(...), 
    repo: AppUserRepo = Depends(AppUserRepo)
    ):
    user = repo.get_user_by_username(username.lower())
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token, refresh_token = token_encoder(user_id=user.user_id)

    # Set the tokens as http-only cookies
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=1800)  # 30 minutes
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=604800)  # 7 days
    return {"message": "Login successful"}

# Logout Endpoint
@app.post("/api/logout/")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logout successful"}

# Check Auth Endpoint
@app.get("/api/check-auth/")
async def check_auth(
    request: Request
    ):
    access_token = request.cookies.get("access_token")
    user_id = decode_token(access_token)
    if access_token and decode_token(access_token):
        return {user_id}
    raise HTTPException(status_code=401, detail="User not authenticated")

app.include_router(school_file_loader.router)
app.include_router(form_submission_router.router) #/form-submissions
app.include_router(admin_user_router.router) #/admin-users, used to create admin, staff or OBC users. 
app.include_router(schools_router.router) #/schools/{school_id}
app.include_router(school_type_router.router) #/schooltypes/{type_id}
app.include_router(school_genre_router.router) #/schoolgenres/{genre_id}
app.include_router(district_router.router) #/districts/{district_id}
app.include_router(grades_router.router) #/grades/{grade_id}
app.include_router(teacher_status_router.router) #/teacherstatuses/{teacher_status_id}
app.include_router(location_router.router) #/locations/{location_id}
app.include_router(app_user_type_router.router) #/usertypes/{type_id}
app.include_router(app_user_router.router) #/app-users/{user_id}
app.include_router(classroom_table_router.router) #/classrooms/{classroom_id}
app.include_router(event_type_router.router) #/event-types/{event_type_id}
app.include_router(event_template_router.router) #/event-templates/{template_id}
app.include_router(event_program_table_router.router) #/events-programs/{event_id}
app.include_router(event_date_table_router.router ) #/event-dates/{date_id}
app.include_router(tickets_status_router.router) #/ticket-statuses/{ticket_status_id}
app.include_router(tickets_table_router.router) #/tickets/{ticket_id}
