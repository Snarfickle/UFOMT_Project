from pydantic import BaseModel
from typing import Union, List
from psycopg.rows import dict_row
from queries.pool import pool

# Input model for SchoolGenre
class SchoolGenreIn(BaseModel):
    type: str
    description: str

# Output model for SchoolGenre
class SchoolGenreOut(SchoolGenreIn):
    genre_id: int

# Repository class for SchoolGenre CRUD operations
class SchoolGenreRepo:
    def create_school_genre(self, school_genre: SchoolGenreIn) -> Union[SchoolGenreOut, dict]:
        # Placeholder SQL interaction to create a new school genre
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO SchoolGenre (
                        type,
                        description)
                        VALUES (%s, %s)
                        RETURNING *;
                    """,
                    [school_genre.type, school_genre.description]
                )
                record = db.fetchone()
                return SchoolGenreOut(**record)
    
    def get_school_genre(self, genre_id: int) -> Union[SchoolGenreOut, dict]:
        # Placeholder SQL interaction to fetch a school genre by its ID
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM SchoolGenre
                    WHERE genre_id = %s;
                    """,
                    [genre_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school genre found with this ID."}
                return SchoolGenreOut(**record)
    def list_school_genre(self) -> Union[List[SchoolGenreOut], dict]:
        # Placeholder SQL interaction to fetch a school genre by its ID
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * 
                    FROM SchoolGenre
                    """
                )
                records = db.fetchall()
                return [SchoolGenreOut(**record) for record in records]
    
    def update_school_genre(self, genre_id: int, school_genre: SchoolGenreIn) -> Union[SchoolGenreOut, dict]:
        # Placeholder SQL interaction to update a school genre by its ID
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE SchoolGenre
                    SET type = %s,
                        description = %s
                    WHERE genre_id = %s
                    RETURNING *;
                    """,
                    [school_genre.type, school_genre.description, genre_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school genre found with this ID."}
                return SchoolGenreOut(**record)
    
    def delete_school_genre(self, genre_id: int) -> dict:
        # Placeholder SQL interaction to delete a school genre by its ID
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM SchoolGenre
                    WHERE genre_id = %s
                    RETURNING *;
                    """,
                    [genre_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No school genre found with this ID."}
                return {"message": "School genre deleted successfully"}
