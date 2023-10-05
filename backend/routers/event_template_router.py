from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from queries.event_template_query import EventTemplateIn, EventTemplateOut, EventTemplateRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new EventTemplate
@router.post("/event-templates", response_model=EventTemplateOut)
@requires_permission(action="create", resource="event-template")  
def create_event_template(
    request: Request,
    event_template: EventTemplateIn,
    repo: EventTemplateRepo = Depends(EventTemplateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.create_event_template(event_template)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a EventTemplate by its ID
@router.get("/event-templates/{template_id}", response_model=EventTemplateOut)
@requires_permission(action="read", resource="event-template")  
def read_event_template(
    request: Request,
    template_id: int,
    repo: EventTemplateRepo = Depends(EventTemplateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_event_template(template_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a EventTemplate by its ID
@router.put("/event-templates/{template_id}", response_model=EventTemplateOut)
@requires_permission(action="update", resource="event-template")  
def update_event_template(
    request: Request,
    template_id: int,
    event_template: EventTemplateIn,
    repo: EventTemplateRepo = Depends(EventTemplateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_event_template(template_id, event_template)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a EventTemplate by its ID
@router.delete("/event-templates/{template_id}", response_model=dict)
@requires_permission(action="delete", resource="event-template")  
def delete_event_template(
    request: Request,
    template_id: int,
    repo: EventTemplateRepo = Depends(EventTemplateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_event_template(template_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all EventTemplates
@router.get("/event-templates", response_model=List[EventTemplateOut])
@requires_permission(action="list", resource="event-template")  
def list_event_templates(
    request: Request,
    repo: EventTemplateRepo = Depends(EventTemplateRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_event_templates()
