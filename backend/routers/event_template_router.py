from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.event_template_query import EventTemplateIn, EventTemplateOut, EventTemplateRepo
# from authenticator import authenticator

router = APIRouter()

# Endpoint to create a new EventTemplate
@router.post("/event-templates", response_model=EventTemplateOut)
def create_event_template(
    event_template: EventTemplateIn,
    repo: EventTemplateRepo = Depends(EventTemplateRepo)
):
    result = repo.create_event_template(event_template)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventTemplate by its ID
@router.get("/event-templates/{template_id}", response_model=EventTemplateOut)
def read_event_template(
    template_id: int,
    repo: EventTemplateRepo = Depends(EventTemplateRepo)
):
    result = repo.get_event_template(template_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventTemplate by its ID
@router.put("/event-templates/{template_id}", response_model=EventTemplateOut)
def update_event_template(
    template_id: int,
    event_template: EventTemplateIn,
    repo: EventTemplateRepo = Depends(EventTemplateRepo)
):
    result = repo.update_event_template(template_id, event_template)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventTemplate by its ID
@router.delete("/event-templates/{template_id}", response_model=dict)
def delete_event_template(
    template_id: int,
    repo: EventTemplateRepo = Depends(EventTemplateRepo)
):
    result = repo.delete_event_template(template_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventTemplates
@router.get("/event-templates", response_model=List[EventTemplateOut])
def list_event_templates(
    repo: EventTemplateRepo = Depends(EventTemplateRepo)
):
    return repo.list_event_templates()
