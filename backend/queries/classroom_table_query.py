from pydantic import BaseModel
from typing import Union, List
from psycopg.rows import dict_row
from queries.pool import pool


# Input model for classroom
class ClassroomIn(BaseModel):
    size: int
    grade_id: int
    teacher_id: int
    drama_mentor_id: int
    art_mentor_id: int
    music_mentor_id: int

# Output model for classroom
class ClassroomOut(ClassroomIn):
    classroom_id: int

class ClassroomRepo:
    def create_classroom(self, classroom: ClassroomIn) -> Union[ClassroomOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO classroom (
                        size,
                        grade_id,
                        teacher_id,
                        drama_mentor_id,
                        art_mentor_id,
                        music_mentor_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING *;
                    """,
                    [
                        classroom.size, classroom.grade_id, classroom.teacher_id, 
                        classroom.drama_mentor_id, classroom.art_mentor_id, classroom.music_mentor_id
                    ]
                )
                record = db.fetchone()
                return ClassroomOut(**record)
    
    def get_classroom(self, classroom_id: int) -> Union[ClassroomOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM classroom
                    WHERE classroom_id = %s;
                    """,
                    [classroom_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No classroom found with this ID."}
                return ClassroomOut(**record)
    
    def update_classroom(self, classroom_id: int, classroom: ClassroomIn) -> Union[ClassroomOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE classroom
                    SET size = %s,
                        grade_id = %s,
                        teacher_id = %s,
                        drama_mentor_id = %s,
                        art_mentor_id = %s,
                        music_mentor_id = %s
                    WHERE classroom_id = %s
                    RETURNING *;
                    """,
                    [
                        classroom.size, classroom.grade_id, classroom.teacher_id, 
                        classroom.drama_mentor_id, classroom.art_mentor_id, classroom.music_mentor_id, classroom_id
                    ]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No classroom found with this ID."}
                return ClassroomOut(**record)
    
    def delete_classroom(self, classroom_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM classroom
                    WHERE classroom_id = %s
                    RETURNING *;
                    """,
                    [classroom_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No classroom found with this ID."}
                return {"message": "classroom deleted successfully"}
    
    def list_classrooms(self) -> List[ClassroomOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM classroom;
                    """
                )
                records = db.fetchall()
                return [ClassroomOut(**record) for record in records]
