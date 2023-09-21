from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.school_genre_query import SchoolGenreIn, SchoolGenreOut, SchoolGenreRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/schoolgenres", response_model=SchoolGenreOut)
def create_school_genre(
    school_genre: SchoolGenreIn,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo)
):
    result = repo.create_school_genre(school_genre)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a SchoolGenre by its ID
@router.get("/schoolgenres/{genre_id}", response_model=SchoolGenreOut)
def read_school_genre(
    genre_id: int,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo)
):
    result = repo.get_school_genre(genre_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a SchoolGenre by its ID
@router.put("/schoolgenres/{genre_id}", response_model=SchoolGenreOut)
def update_school_genre(
    genre_id: int,
    school_genre: SchoolGenreIn,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo)
):
    result = repo.update_school_genre(genre_id, school_genre)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a SchoolGenre by its ID
@router.delete("/schoolgenres/{genre_id}", response_model=dict)
def delete_school_genre(
    genre_id: int,
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo)
):
    result = repo.delete_school_genre(genre_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all SchoolGenres
@router.get("/schoolgenres", response_model=List[SchoolGenreOut])
def list_school_genres(
    repo: SchoolGenreRepo = Depends(SchoolGenreRepo)
):
    return repo.list_school_genre()
