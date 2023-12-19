from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

# Define input model for SchoolType
class SchoolTypeIn(BaseModel):
    type: str
    description: str

# Define output model for SchoolType
class SchoolTypeOut(SchoolTypeIn):
    type_id: int

# Extend the current structure to include CRUD for SchoolType
class SchoolTypeRepo:
    def create_school_type(self, school_type: SchoolTypeIn) -> Union[SchoolTypeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO SchoolType (
                        type,
                        description)
                        VALUES (%s, %s)
                        RETURNING *;
                    """,
                    [school_type.type, school_type.description]
                )
                record = db.fetchone()
                return SchoolTypeOut(**record)
    
    def get_school_type(self, type_id: int) -> Union[SchoolTypeOut, dict]:
        # Placeholder SQL interaction to fetch a school type by its ID
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM SchoolType
                    WHERE type_id = %s;
                    """,
                    [type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school type found with this ID."}
                return SchoolTypeOut(**record)
    
    def list_school_type(self) -> Union[List[SchoolTypeOut], dict]:
        # Placeholder SQL interaction to fetch a list of school types
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * 
                    FROM SchoolType
                    """
                )
                records = db.fetchall()
                return [SchoolTypeOut(**record) for record in records]

    def update_school_type(self, type_id: int, school_type: SchoolTypeIn) -> Union[SchoolTypeOut, dict]:
        # Placeholder SQL interaction to update a school type by its ID
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE SchoolType
                    SET type = %s,
                        description = %s
                    WHERE type_id = %s
                    RETURNING *;
                    """,
                    [school_type.type, school_type.description, type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school type found with this ID."}
                return SchoolTypeOut(**record)
    
    def delete_school_type(self, type_id: int) -> dict:
        # Placeholder SQL interaction to delete a school type by its ID
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM SchoolType
                    WHERE type_id = %s
                    RETURNING *;
                    """,
                    [type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school type found with this ID."}
                return {"message": "School type deleted successfully"}
