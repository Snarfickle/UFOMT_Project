from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.grades_query import GradeIn, GradeOut, GradeRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/grades", response_model=GradeOut)
def create_grade(
    grade: GradeIn,
    repo: GradeRepo = Depends(GradeRepo)
):
    result = repo.create_grade(grade)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Grade by its ID
@router.get("/grades/{grade_id}", response_model=GradeOut)
def read_grade(
    grade_id: int,
    repo: GradeRepo = Depends(GradeRepo)
):
    result = repo.get_grade(grade_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Grade by its ID
@router.put("/grades/{grade_id}", response_model=GradeOut)
def update_grade(
    grade_id: int,
    grade: GradeIn,
    repo: GradeRepo = Depends(GradeRepo)
):
    result = repo.update_grade(grade_id, grade)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Grade by its ID
@router.delete("/grades/{grade_id}", response_model=dict)
def delete_grade(
    grade_id: int,
    repo: GradeRepo = Depends(GradeRepo)
):
    result = repo.delete_grade(grade_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Grades
@router.get("/grades", response_model=List[GradeOut])
def list_grades(
    repo: GradeRepo = Depends(GradeRepo)
):
    return repo.list_grades()
