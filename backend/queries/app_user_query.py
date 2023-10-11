from pydantic import BaseModel
from typing import Optional, Union, List
from datetime import date, datetime
from queries.pool import pool
from psycopg.rows import dict_row

# Input model for AppUser
class AppUserIn(BaseModel):
    username: str
    password: str
    type_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: int
    created_date: Optional[date] = None
    terminated_date: Optional[date] = None
    grade_id: Optional[int] = None
    school_id: Optional[int] = None
    cactus_id: Optional[str] = None
    active: Optional[bool] = None
    notes: Optional[str] = None
    teacher_status_id: Optional[int] = None
    parent_guardian: Optional[str] = None
    employee_id: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None




# Output model for AppUser
class AppUserOut(AppUserIn):
    user_id: int
    updated_at: datetime



class AppUserRepo:

    def create_app_user(self, user: AppUserIn) -> Union[AppUserOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                # SQL query for inserting an app user
                db.execute(
                    """
                    INSERT INTO app_user (
                        username, 
                        password,
                        type_id,
                        first_name,
                        last_name,
                        email,
                        phone_number,
                        created_date,
                        terminated_date,
                        grade_id,
                        school_id,
                        cactus_id,
                        active,
                        notes,
                        teacher_status_id,
                        parent_guardian,
                        employee_id,
                        street,
                        city,
                        state,
                        zip
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *;
                    """,
                    [
                        user.username,
                        user.password,
                        user.type_id,
                        user.first_name,
                        user.last_name,
                        user.email,
                        user.phone_number,
                        user.created_date,
                        user.terminated_date,
                        user.grade_id,
                        user.school_id,
                        user.cactus_id,
                        user.active,
                        user.notes,
                        user.teacher_status_id,
                        user.parent_guardian,
                        user.employee_id,
                        user.street,
                        user.city,
                        user.state,
                        user.zip
                    ]
                )
                record = db.fetchone()
                return AppUserOut(**record)

    def get_app_user(self, user_id: int) -> Union[AppUserOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                # SQL query for fetching an app user by ID
                db.execute(
                    """
                    SELECT * FROM app_user
                    WHERE user_id = %s;
                    """,
                    [user_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No app user found with this ID."}
                return AppUserOut(**record)
            
    def update_app_user(self, user_id: int, user: AppUserIn) -> Union[AppUserOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                # SQL query for updating an app user by ID
                db.execute(
                    """
                    UPDATE app_user
                    SET 
                    username = %s,
                    password = %s,
                    type_id = %s,
                    first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone_number = %s,
                    created_date = %s,
                    terminated_date = %s,
                    grade_id = %s,
                    school_id = %s,
                    cactus_id = %s,
                    active = %s,
                    notes = %s,
                    teacher_status_id = %s,
                    parent_guardian = %s,
                    employee_id = %s,
                    street = %s,
                    city = %s,
                    state = %s,
                    zip = %s
                    WHERE user_id = %s
                    RETURNING *;
                    """,
                    [
                        user.username,
                        user.password,
                        user.type_id,
                        user.first_name,
                        user.last_name,
                        user.email,
                        user.phone_number,
                        user.created_date,
                        user.terminated_date,
                        user.grade_id,
                        user.school_id,
                        user.cactus_id,
                        user.active,
                        user.notes,
                        user.teacher_status_id,
                        user.parent_guardian,
                        user.employee_id,
                        user.street,
                        user.city,
                        user.state,
                        user.zip,
                        user_id
                    ]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No app user found with this ID."}
                return AppUserOut(**record)
            
    def delete_app_user(self, user_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                # SQL query for deleting an app user by ID
                db.execute(
                    """
                    DELETE FROM app_user
                    WHERE user_id = %s
                    RETURNING *;
                    """,
                    [user_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No app user found with this ID."}
                return {"message": "App user deleted successfully"}
    def list_app_users(self) -> List[AppUserOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM app_user;
                    """
                )
                records = db.fetchall()
                return [AppUserOut(**record) for record in records]
    def get_user_by_username(self, username: str) -> Union[AppUserOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM app_user
                    WHERE username = %s;
                    """,
                    [username]
                )
                record = db.fetchone()
                if record is None:
                    return None
                return AppUserOut(**record)
    def check_permission_query(self, user_type_id: int, action: str, resource: str) -> bool:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                # SQL query to check permission
                db.execute(
                    """
                    SELECT can_access FROM permission
                    JOIN action ON permission.action_id = action.action_id
                    JOIN resource ON permission.resource_id = resource.resource_id
                    WHERE permission.type_id = %s AND resource.name = %s AND action.name = %s;
                    """,
                    [user_type_id, resource, action]
                )
                record = db.fetchone()
                # If no record is found or can_access is False, return False
                if record is None or not record['can_access']:
                    return False
                return True
