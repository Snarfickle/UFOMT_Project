from fastapi import APIRouter, HTTPException, Request, Depends
from typing import List
from queries.form_submission_query import FormSubmissionIn, FormSubmissionOut, FormSubmissionRepo
from auth_utils.auth_utils import requires_permission, get_current_user
from queries.app_user_query import AppUserIn

router = APIRouter()

# Endpoint to create a new FormSubmission
@router.post("/api/form-submissions", response_model=FormSubmissionOut)
def create_form_submission(
    submission: FormSubmissionIn,
    repo: FormSubmissionRepo = Depends(FormSubmissionRepo)
):
    print("submission: ",submission)
    result = repo.create_submission(submission)
    # if "error" in result:
    #     raise HTTPException(status_code=400, detail=result["error"])
    return result

# Endpoint to fetch a FormSubmission by its ID
@router.get("/api/form-submissions/{submission_id}", response_model=FormSubmissionOut)
@requires_permission(action="read", resource="form-submission")
def read_form_submission(
    request: Request,
    submission_id: int,
    repo: FormSubmissionRepo = Depends(FormSubmissionRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.get_submission(submission_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to update a FormSubmission by its ID
@router.put("/api/form-submissions/{submission_id}", response_model=FormSubmissionOut)
@requires_permission(action="update", resource="form-submission")
def update_form_submission(
    request: Request,
    submission_id: int,
    submission: FormSubmissionIn,
    repo: FormSubmissionRepo = Depends(FormSubmissionRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.update_submission(submission_id, submission)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to delete a FormSubmission by its ID
@router.delete("/api/form-submissions/{submission_id}", response_model=dict)
@requires_permission(action="delete", resource="form-submission")
def delete_form_submission(
    request: Request,
    submission_id: int,
    repo: FormSubmissionRepo = Depends(FormSubmissionRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    result = repo.delete_submission(submission_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# Endpoint to list all FormSubmissions
@router.get("/api/form-submissions", response_model=List[FormSubmissionOut])
@requires_permission(action="list", resource="form-submission")
def list_form_submissions(
    request: Request,
    repo: FormSubmissionRepo = Depends(FormSubmissionRepo),
    current_user: AppUserIn = Depends(get_current_user)
):
    return repo.list_submissions()
