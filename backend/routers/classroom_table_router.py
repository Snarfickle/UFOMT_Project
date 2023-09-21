from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.classroom_table_query import ClassroomIn, ClassroomOut, ClassroomRepo
# from authenticator import authenticator

router = APIRouter()

@router.post("/classrooms", response_model=ClassroomOut)
def create_classroom(
    classroom: ClassroomIn,
    repo: ClassroomRepo = Depends(ClassroomRepo)
):
    result = repo.create_classroom(classroom)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a Classroom by its ID
@router.get("/classrooms/{classroom_id}", response_model=ClassroomOut)
def read_classroom(
    classroom_id: int,
    repo: ClassroomRepo = Depends(ClassroomRepo)
):
    result = repo.get_classroom(classroom_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a Classroom by its ID
@router.put("/classrooms/{classroom_id}", response_model=ClassroomOut)
def update_classroom(
    classroom_id: int,
    classroom: ClassroomIn,
    repo: ClassroomRepo = Depends(ClassroomRepo)
):
    result = repo.update_classroom(classroom_id, classroom)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a Classroom by its ID
@router.delete("/classrooms/{classroom_id}", response_model=dict)
def delete_classroom(
    classroom_id: int,
    repo: ClassroomRepo = Depends(ClassroomRepo)
):
    result = repo.delete_classroom(classroom_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all Classrooms
@router.get("/classrooms", response_model=List[ClassroomOut])
def list_classrooms(
    repo: ClassroomRepo = Depends(ClassroomRepo)
):
    return repo.list_classrooms()
