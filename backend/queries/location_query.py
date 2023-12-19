from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool

# Input model for location
class LocationIn(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip: int
    location_description: Optional[str] = None

# Output model for location
class LocationOut(LocationIn):
    location_id: int

class LocationRepo:
    def create_location(self, location: LocationIn) -> Union[LocationOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO location (
                        name,
                        address,
                        city,
                        state,
                        zip,
                        location_description)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING *;
                    """,
                    [location.name, location.address, location.city, location.state, location.zip, location.location_description]
                )
                record = db.fetchone()
                return LocationOut(**record)
    
    def get_location(self, location_id: int) -> Union[LocationOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM location
                    WHERE location_id = %s;
                    """,
                    [location_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No location found with this ID."}
                return LocationOut(**record)
    
    def update_location(self, location_id: int, location: LocationIn) -> Union[LocationOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE location
                    SET name = %s,
                        address = %s,
                        city = %s,
                        state = %s,
                        zip = %s,
                        location_description = %s
                    WHERE location_id = %s
                    RETURNING *;
                    """,
                    [location.name, location.address, location.city, location.state, location.zip, location.location_description, location_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No location found with this ID."}
                return LocationOut(**record)
    
    def delete_location(self, location_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM location
                    WHERE location_id = %s
                    RETURNING *;
                    """,
                    [location_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No location found with this ID."}
                return {"message": "Location deleted successfully"}
    
    def list_locations(self) -> List[LocationOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM location;
                    """
                )
                records = db.fetchall()
                return [LocationOut(**record) for record in records]
