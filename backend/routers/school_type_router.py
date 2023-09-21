from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List
from queries.school_type_query import SchoolTypeIn, SchoolTypeOut, SchoolTypeRepo

router = APIRouter()

# Endpoint to create a new SchoolType
@router.post("/schooltypes", response_model=SchoolTypeOut)
def create_school_type(
    school_type: SchoolTypeIn,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo)
):
    result = repo.create_school_type(school_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to get a SchoolType by its ID
@router.get("/schooltypes/{type_id}", response_model=SchoolTypeOut)
def read_school_type(
    type_id: int,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo)
):
    result = repo.get_school_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to get a list of SchoolTypes
@router.get("/schooltypes", response_model=List[SchoolTypeOut])
def list_school_type(
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo)
):
    result = repo.list_school_type()
    print("result:    -", result)
    return result

# Endpoint to update a SchoolType by its ID
@router.put("/schooltypes/{type_id}", response_model=SchoolTypeOut)
def update_school_type(
    type_id: int,
    school_type: SchoolTypeIn,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo)
):
    result = repo.update_school_type(type_id, school_type)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a SchoolType by its ID
@router.delete("/schooltypes/{type_id}", response_model=dict)
def delete_school_type(
    type_id: int,
    repo: SchoolTypeRepo = Depends(SchoolTypeRepo)
):
    result = repo.delete_school_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
