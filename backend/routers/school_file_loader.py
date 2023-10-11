from fastapi import File, UploadFile, HTTPException, APIRouter
import csv
import io
from psycopg.rows import dict_row
from queries.pool import pool


router = APIRouter()

@router.post("/uploadschools")
async def upload_schools_file(file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        data = await file.read()
        reader = csv.DictReader(io.StringIO(data.decode('utf-8')))
        
        # Database insertion
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                for row in reader:
                    # Check if type is "Charter" and adjust district_name accordingly
                    type_name = row['type']
                    district_name = row['district_name']

                    if type_name.lower() == "charter":
                        district_name = "Charter"
                    elif type_name.lower() == "private":
                        district_name = "Private"
                    
                    # Fetch district_id using district name
                    db.execute("SELECT district_id FROM District WHERE name = %s", (district_name,))
                    district_id = db.fetchone()
                    
                    # Insert new district if not found
                    if not district_id:
                        db.execute(
                            """
                            INSERT INTO District (name, zipcode) VALUES (%s, %s)
                            RETURNING district_id;
                            """,
                            [district_name, row['zip']]
                        )
                        district_id = db.fetchone()
                    else:
                        district_id = district_id['district_id'] # There are some issues here when uploading the file. I had to remove the else statement here to include the special edge cases. I re-implemented it in order to include all of the rest (the rest of the schools on the list).


                    # Fetch type_id using type name
                    db.execute("SELECT type_id FROM SchoolType WHERE type = %s", (type_name,))
                    type_id = db.fetchone()
                    if type_id:
                        type_id = type_id['type_id']
                    
                    # Check if district_id and type_id were found
                    if district_id and type_id:
                        try:
                            db.execute(
                                """
                                INSERT INTO School (
                                    name, phone, street, city, zip, 
                                    title_one_status, district_id, type_id
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (name, district_id) DO NOTHING
                                RETURNING *;
                                """,
                                [
                                    row['name'], row['phone'], row['street'], row['city'], row['zip'], row['title_one_status'], district_id, type_id
                                ]
                            )
                            new_school = db.fetchone()
                        except Exception as e:
                            print(f"Failed to insert school {row['name']} in district {district_name}. Error: {str(e)}")
                            # Optionally, log the error to a file or monitoring system
                            continue
                    else:
                        print(f"Warning: District {district_name} or Type {type_name} not found, skipping entry for {row['name']}.")
    return {"status": "ok"}
    
@router.post("/uploaddistricts")
async def upload_districts_file(file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        data = await file.read()
        reader = csv.DictReader(io.StringIO(data.decode('utf-8')))
        
        # Database insertion
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                for row in reader:
                    # Fetch district_id using district name
                    db.execute("SELECT district_id FROM District WHERE name = %s", (row['district_name'],))
                    district_id = db.fetchone()
                    
                    # Check if district_id was found
                    if district_id:
                        pass
                        print(f"District found in database, proceeding onto the next value in file")
                    else:
                        # Handle case where district is not found
                        print(f"Warning: District {row['district_name']} not found, creating new district and retrying school entry.")
                        
                        # Insert new district
                        db.execute(
                            """
                            INSERT INTO District (name, zipcode) VALUES (%s, %s)
                            RETURNING district_id;
                            """,
                            [row['district_name'], row['zipcode']]
                        )
                        new_district = db.fetchone()
                        print(f"Inserted new district: {new_district}")
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
