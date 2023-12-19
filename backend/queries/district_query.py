from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

class DistrictIn(BaseModel):
    name: str
    zipcode: int

# Output model for District
class DistrictOut(DistrictIn):
    district_id: int

# Repository class for District CRUD operations
class DistrictRepo:
    def create_district(self, district: DistrictIn) -> Union[DistrictOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO District (
                        name,
                        zipcode)
                        VALUES (%s, %s)
                        RETURNING *;
                    """,
                    [district.name, district.zipcode]
                )
                record = db.fetchone()
                return DistrictOut(**record)
    
    def get_district(self, district_id: int) -> Union[DistrictOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM District
                    WHERE district_id = %s;
                    """,
                    [district_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No district found with this ID."}
                return DistrictOut(**record)
    
    def update_district(self, district_id: int, district: DistrictIn) -> Union[DistrictOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE District
                    SET name = %s,
                        zipcode = %s
                    WHERE district_id = %s
                    RETURNING *;
                    """,
                    [district.name, district.zipcode, district_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No district found with this ID."}
                return DistrictOut(**record)
    
    def delete_district(self, district_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM District
                    WHERE district_id = %s
                    RETURNING *;
                    """,
                    [district_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No district found with this ID."}
                return {"message": "District deleted successfully"}
    
    def list_districts(self) -> List[DistrictOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM District;
                    """
                )
                records = db.fetchall()
                return [DistrictOut(**record) for record in records]
