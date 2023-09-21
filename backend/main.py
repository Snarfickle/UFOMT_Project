from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from queries import app_user_query
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
)

app = FastAPI()

User = app_user_query.AppUserIn

def fake_decode_token(token):
    return User(
        email=token + "fakedecoded", full_name="John Doe"
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/items/")
async def read_root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

app.include_router(schools_router.router)
app.include_router(school_type_router.router)
app.include_router(school_genre_router.router)
app.include_router(district_router.router)
app.include_router(grades_router.router)
app.include_router(teacher_status_router.router)
app.include_router(location_router.router)
app.include_router(app_user_type_router.router)
app.include_router(app_user_router.router)
app.include_router(classroom_table_router.router)
app.include_router(event_type_router.router)
app.include_router(event_template_router.router)
app.include_router(event_program_table_router.router)
app.include_router(event_date_table_router.router)
app.include_router(tickets_status_router.router)
app.include_router(tickets_table_router.router)
