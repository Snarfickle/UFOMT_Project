from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.teacher_status_query import TeacherStatusIn, TeacherStatusOut, TeacherStatusRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/teacherstatuses", response_model=TeacherStatusOut)
def create_teacher_status(
    teacher_status: TeacherStatusIn,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo)
):
    result = repo.create_teacher_status(teacher_status)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a TeacherStatus by its ID
@router.get("/teacherstatuses/{teacher_status_id}", response_model=TeacherStatusOut)
def read_teacher_status(
    teacher_status_id: int,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo)
):
    result = repo.get_teacher_status(teacher_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a TeacherStatus by its ID
@router.put("/teacherstatuses/{teacher_status_id}", response_model=TeacherStatusOut)
def update_teacher_status(
    teacher_status_id: int,
    teacher_status: TeacherStatusIn,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo)
):
    result = repo.update_teacher_status(teacher_status_id, teacher_status)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a TeacherStatus by its ID
@router.delete("/teacherstatuses/{teacher_status_id}", response_model=dict)
def delete_teacher_status(
    teacher_status_id: int,
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo)
):
    result = repo.delete_teacher_status(teacher_status_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all TeacherStatuses
@router.get("/teacherstatuses", response_model=List[TeacherStatusOut])
def list_teacher_statuses(
    repo: TeacherStatusRepo = Depends(TeacherStatusRepo)
):
    return repo.list_teacher_statuses()
