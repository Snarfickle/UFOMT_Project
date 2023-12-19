from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.teacher_status_query import TeacherStatusIn, TeacherStatusOut, TeacherStatusRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

@router.post("/api/teacherstatuses", response_model=TeacherStatusOut)
@requires_permission(action="create", resource="teacher-status") 
def create_teacher_status(
    request: Request,
    teacher_status: TeacherStatusIn,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_teacher_status(teacher_status)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a TeacherStatus by its ID
@router.get("/api/teacherstatuses/{teacher_status_id}", response_model=TeacherStatusOut)
@requires_permission(action="read", resource="teacher-status") 
def read_teacher_status(
    request: Request,
    teacher_status_id: int,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_teacher_status(teacher_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a TeacherStatus by its ID
@router.put("/api/teacherstatuses/{teacher_status_id}", response_model=TeacherStatusOut)
@requires_permission(action="update", resource="teacher-status") 
def update_teacher_status(
    request: Request,
    teacher_status_id: int,
    teacher_status: TeacherStatusIn,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_teacher_status(teacher_status_id, teacher_status)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a TeacherStatus by its ID
@router.delete("/api/teacherstatuses/{teacher_status_id}", response_model=dict)
@requires_permission(action="delete", resource="teacher-status") 
def delete_teacher_status(
    request: Request,
    teacher_status_id: int,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_teacher_status(teacher_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all TeacherStatuses
@router.get("/api/teacherstatuses", response_model=List[TeacherStatusOut])
@requires_permission(action="list", resource="teacher-status") 
def list_teacher_statuses(
    request: Request,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_teacher_statuses()
