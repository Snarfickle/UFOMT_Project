from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool


# Input model for UserType
class UserTypeIn(BaseModel):
    type: str
    description: str

# Output model for UserType
class UserTypeOut(UserTypeIn):
    type_id: int

class UserTypeRepo:
    def create_user_type(self, user_type: UserTypeIn) -> Union[UserTypeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO UserType (
                        type,
                        description)
                        VALUES (%s, %s)
                        RETURNING *;
                    """,
                    [user_type.type, user_type.description]
                )
                record = db.fetchone()
                return UserTypeOut(**record)
    
    def get_user_type(self, type_id: int) -> Union[UserTypeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM UserType
                    WHERE type_id = %s;
                    """,
                    [type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No UserType found with this ID."}
                return UserTypeOut(**record)
    
    def update_user_type(self, type_id: int, user_type: UserTypeIn) -> Union[UserTypeOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE UserType
                    SET type = %s,
                        description = %s
                    WHERE type_id = %s
                    RETURNING *;
                    """,
                    [user_type.type, user_type.description, type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No UserType found with this ID."}
                return UserTypeOut(**record)
    
    def delete_user_type(self, type_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM UserType
                    WHERE type_id = %s
                    RETURNING *;
                    """,
                    [type_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No UserType found with this ID."}
                return {"message": "UserType deleted successfully"}
    
    def list_user_types(self) -> List[UserTypeOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM UserType;
                    """
                )
                records = db.fetchall()
                return [UserTypeOut(**record) for record in records]
