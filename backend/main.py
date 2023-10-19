from fastapi import FastAPI, Depends, HTTPException, Form
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
# from start_file import create_initial_user


app = FastAPI()

origins = [
    "http://localhost:3000",  # React local dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["http://localhost:3000"],  # Allows requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# @app.on_event("startup")
# async def startup_event():

#     # Your script logic here
#         create_initial_user()

def hash_password(plain_password: str) -> str:
    # '''Hash a password for storing.'''
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # '''Check hashed password. Using bcrypt, the salt is saved into the hash itself.'''
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Endpoint to login and get a JWT token
@app.post("/login/", response_model=Token)
def login_for_access_token(username: str = Form(...), password: str = Form(...), repo: AppUserRepo = Depends(AppUserRepo)):
    user = repo.get_user_by_username(username.lower())
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = token_encoder(user_id=user.user_id)
    return {"access_token":access_token, "token_type":"bearer"}

@app.post("/token/", response_model=Token)
def login_for_access_token(username: str = Form(...), password: str = Form(...), repo: AppUserRepo = Depends(AppUserRepo)):
    user = repo.get_user_by_username(username.lower())
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = token_encoder(user_id=user.user_id)
    return {"access_token":access_token, "token_type":"bearer"}

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
