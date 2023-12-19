from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.classroom_table_query import ClassroomIn, ClassroomOut, ClassroomRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

@router.post("/api/classrooms", response_model=ClassroomOut)
@requires_permission(action="create", resource="classroom")  
def create_classroom(
    request: Request,
    classroom: ClassroomIn,
    repo: ClassroomRepo = Depends(ClassroomRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_classroom(classroom)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Classroom by its ID
@router.get("/api/classrooms/{classroom_id}", response_model=ClassroomOut)
@requires_permission(action="read", resource="classroom")  
def read_classroom(
    request: Request,
    classroom_id: int,
    repo: ClassroomRepo = Depends(ClassroomRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_classroom(classroom_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Classroom by its ID
@router.put("/api/classrooms/{classroom_id}", response_model=ClassroomOut)
@requires_permission(action="update", resource="classroom")  
def update_classroom(
    request: Request,
    classroom_id: int,
    classroom: ClassroomIn,
    repo: ClassroomRepo = Depends(ClassroomRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_classroom(classroom_id, classroom)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Classroom by its ID
@router.delete("/api/classrooms/{classroom_id}", response_model=dict)
@requires_permission(action="delete", resource="classroom")  
def delete_classroom(
    request: Request,
    classroom_id: int,
    repo: ClassroomRepo = Depends(ClassroomRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_classroom(classroom_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Classrooms
@router.get("/api/classrooms", response_model=List[ClassroomOut])
@requires_permission(action="list", resource="classroom")  
def list_classrooms(
    request: Request,
    repo: ClassroomRepo = Depends(ClassroomRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_classrooms()
