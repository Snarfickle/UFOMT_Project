from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.school_genre_query import SchoolGenreIn, SchoolGenreOut, SchoolGenreRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn


router = APIRouter()

@router.post("/schoolgenres", response_model=SchoolGenreOut)
@requires_permission(action="create", resource="school-genre")  
def create_school_genre(
    request: Request,
    school_genre: SchoolGenreIn,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_school_genre(school_genre)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a SchoolGenre by its ID
@router.get("/schoolgenres/{genre_id}", response_model=SchoolGenreOut)
@requires_permission(action="read", resource="school-genre")  
def read_school_genre(
    request: Request,
    genre_id: int,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_school_genre(genre_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a SchoolGenre by its ID
@router.put("/schoolgenres/{genre_id}", response_model=SchoolGenreOut)
@requires_permission(action="update", resource="school-genre")  
def update_school_genre(
    request: Request,
    genre_id: int,
    school_genre: SchoolGenreIn,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_school_genre(genre_id, school_genre)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a SchoolGenre by its ID
@router.delete("/schoolgenres/{genre_id}", response_model=dict)
@requires_permission(action="delete", resource="school-genre")  
def delete_school_genre(
    request: Request,
    genre_id: int,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_school_genre(genre_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all SchoolGenres
@router.get("/schoolgenres", response_model=List[SchoolGenreOut])
@requires_permission(action="list", resource="school-genre")  
def list_school_genres(
    request: Request,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_school_genre()
