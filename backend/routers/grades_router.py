from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.grades_query import GradeIn, GradeOut, GradeRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

@router.post("/grades", response_model=GradeOut)
@requires_permission(action="create", resource="grades") 
def create_grade(
    request: Request,
    grade: GradeIn,
    repo: GradeRepo = Depends(GradeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_grade(grade)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Grade by its ID
@router.get("/grades/{grade_id}", response_model=GradeOut)
@requires_permission(action="read", resource="grades") 
def read_grade(
    request: Request,
    grade_id: int,
    repo: GradeRepo = Depends(GradeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_grade(grade_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Grade by its ID
@router.put("/grades/{grade_id}", response_model=GradeOut)
@requires_permission(action="update", resource="grades") 
def update_grade(
    request: Request,
    grade_id: int,
    grade: GradeIn,
    repo: GradeRepo = Depends(GradeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_grade(grade_id, grade)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Grade by its ID
@router.delete("/grades/{grade_id}", response_model=dict)
@requires_permission(action="delete", resource="grades") 
def delete_grade(
    request: Request,
    grade_id: int,
    repo: GradeRepo = Depends(GradeRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_grade(grade_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Grades
@router.get("/grades", response_model=List[GradeOut])
# @requires_permission(action="list", resource="grades") 
def list_grades(
    request: Request,
    repo: GradeRepo = Depends(GradeRepo)
    # current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_grades()
