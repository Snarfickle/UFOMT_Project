from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

class TeacherStatusIn(BaseModel):
    status: str
    description: str

# Output model for teacher_status
class TeacherStatusOut(TeacherStatusIn):
    teacher_status_id: int

# Repository class for teacher_status CRUD operations
class TeacherStatusRepo:
    def create_teacher_status(self, teacher_status: TeacherStatusIn) -> Union[TeacherStatusOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO teacher_status (
                        status,
                        description)
                        VALUES (%s, %s)
                        RETURNING *;
                    """,
                    [teacher_status.status, teacher_status.description]
                )
                record = db.fetchone()
                return TeacherStatusOut(**record)
    
    def get_teacher_status(self, teacher_status_id: int) -> Union[TeacherStatusOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM teacher_status
                    WHERE teacher_status_id = %s;
                    """,
                    [teacher_status_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No teacher_status found with this ID."}
                return TeacherStatusOut(**record)
    
    def update_teacher_status(self, teacher_status_id: int, teacher_status: TeacherStatusIn) -> Union[TeacherStatusOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE teacher_status
                    SET status = %s,
                        description = %s
                    WHERE teacher_status_id = %s
                    RETURNING *;
                    """,
                    [teacher_status.status, teacher_status.description, teacher_status_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No teacher_status found with this ID."}
                return TeacherStatusOut(**record)
    
    def delete_teacher_status(self, teacher_status_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM teacher_status
                    WHERE teacher_status_id = %s
                    RETURNING *;
                    """,
                    [teacher_status_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No teacher_status found with this ID."}
                return {"message": "Teacher status deleted successfully"}
    
    def list_teacher_statuses(self) -> List[TeacherStatusOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM teacher_status;
                    """
                )
                records = db.fetchall()
                return [TeacherStatusOut(**record) for record in records]
