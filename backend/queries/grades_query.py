from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

class GradeIn(BaseModel):
    grade: str
    description: str

# Output model for grades
class GradeOut(GradeIn):
    grade_id: int

# Repository class for grades CRUD operations
class GradeRepo:
    def create_grade(self, grade: GradeIn) -> Union[GradeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO grades (
                        grade,
                        description)
                        VALUES (%s, %s)
                        RETURNING *;
                    """,
                    [grade.grade, grade.description]
                )
                record = db.fetchone()
                return GradeOut(**record)
    
    def get_grade(self, grade_id: int) -> Union[GradeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM grades
                    WHERE grade_id = %s;
                    """,
                    [grade_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No grade found with this ID."}
                return GradeOut(**record)
    
    def update_grade(self, grade_id: int, grade: GradeIn) -> Union[GradeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE grades
                    SET grade = %s,
                        description = %s
                    WHERE grade_id = %s
                    RETURNING *;
                    """,
                    [grade.grade, grade.description, grade_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No grade found with this ID."}
                return GradeOut(**record)
    
    def delete_grade(self, grade_id: int) -> dict:

        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM grades
                    WHERE grade_id = %s
                    RETURNING *;
                    """,
                    [grade_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No grade found with this ID."}
                return {"message": "Grade deleted successfully"}
    
    def list_grades(self) -> List[GradeOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM grades;
                    """
                )
                records = db.fetchall()
                return [GradeOut(**record) for record in records]
