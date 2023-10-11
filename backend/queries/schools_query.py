from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool
from psycopg.rows import dict_row
from datetime import datetime


class Error(BaseModel):
    message: str

class SchoolIn(BaseModel):
    name: str
    phone: str
    street: str
    city: str
    state: Optional[str] = None
    zip: str
    student_body_count: Optional[int] = None
    title_one_status: Optional[bool] = None
    district_id: int
    type_id: Optional[int] = None
    genre_id: Optional[int] = None


class SchoolOut(SchoolIn):
    school_id: int
    created_at: datetime
    updated_at: datetime


class SchoolRepo:
    def create_school(self, school: SchoolIn) -> Union[SchoolOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO School (
                        name,
                        phone,
                        street,
                        city,
                        state,
                        zip,
                        student_body_count,
                        title_one_status,
                        district_id,
                        type_id,
                        genre_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING *;
                    """,
                    [school.name,
                     school.phone,
                     school.street,
                     school.city,
                     school.state,
                     school.zip,
                     school.student_body_count,
                     school.title_one_status,
                     school.district_id,
                     school.type_id,
                     school.genre_id]
                     )
                record = db.fetchone()
                return SchoolOut(**record)
            
    def get_school(self, school_id:int) -> Union[SchoolOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM School
                    WHERE school_id = %s
                    """,
                    [school_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school found with this ID."}
                return SchoolOut(**record)
    def get_all_schools(self) -> Union[List[SchoolOut], dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM School
                    """
                )
                records = db.fetchall()
                return [SchoolOut(**record) for record in records]
    def update_school(self, school_id:int, school: SchoolIn) ->Union[SchoolOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE School
                    SET name = %s,
                        phone = %s,
                        street = %s,
                        city = %s,
                        state = %s,
                        zip = %s,
                        student_body_count = %s,
                        title_one_status = %s,
                        district_id = %s,
                        type_id = %s,
                        genre_id = %s
                    WHERE school_id = %s
                    RETURNING *;
                    """,
                    [school.name,
                     school.phone,
                     school.street,
                     school.city,
                     school.state,
                     school.zip,
                     school.student_body_count,
                     school.title_one_status,
                     school.district_id,
                     school.type_id,
                     school.genre_id,
                     school_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school found with this ID."}
                return SchoolOut(**record)
    def delete_school(self, school_id:int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM School
                    WHERE school_id = %s
                    RETURNING *;
                    """,
                    [school_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school found with this ID."}
                return {"message": "School deleted successfully"}
