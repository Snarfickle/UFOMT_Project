from pydantic import BaseModel
from typing import Optional, Union, List
from psycopg.rows import dict_row
from queries.pool import pool
from psycopg2 import IntegrityError, DatabaseError
import logging

# Input model for FormSubmissions
class FormSubmissionIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    teacher_status: bool
    cactus_number: Optional[str] = None
    guardian_name: Optional[str] = None
    classroom_size: Optional[int] = None
    number_of_classrooms: Optional[int] = None
    event_program_id: int
    event_date_id: int
    school_id: int
    school_type_id: Optional[int] = None
    school_genre_id: Optional[int] = None
    grade_id: int
    additional_contact: bool

# Output model for FormSubmissions
class FormSubmissionOut(FormSubmissionIn):
    submission_id: int 

class FormSubmissionRepo:
    def create_submission(self, submission: FormSubmissionIn) -> Union[FormSubmissionOut, dict]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        INSERT INTO FormSubmissions (
                            first_name,
                            last_name,
                            email,
                            phone_number,
                            teacher_status,
                            cactus_number,
                            guardian_name,
                            classroom_size,
                            number_of_classrooms,
                            event_program_id,
                            event_date_id,
                            school_id,
                            school_type_id,
                            school_genre_id,
                            grade_id,
                            additional_contact)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING *;
                        """,
                        [
                            submission.first_name, submission.last_name, submission.email, 
                            submission.phone_number, submission.teacher_status, submission.cactus_number, submission.guardian_name, submission.classroom_size, 
                            submission.number_of_classrooms, submission.event_program_id, submission.event_date_id, 
                            submission.school_id, submission.school_type_id, submission.school_genre_id, 
                            submission.grade_id, submission.additional_contact
                        ]
                    )
                    record = db.fetchone()

                    return FormSubmissionOut(**record)
        except IntegrityError as e:
            logging.error(f"Integrity Error: {str(e)}")
            return {"error": "A record with these details may already exist or you're violating a database constraint. Please check your data and try again."}

        except DatabaseError as e:
            logging.error(f"Database Error: {str(e)}")
            return {"error": "An error occurred with the database. Please try again later."}

        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")
            return {"error": "An unexpected error occurred. Please try again later."}
    
    def get_submission(self, submission_id: int) -> Union[FormSubmissionOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM FormSubmissions
                    WHERE submission_id = %s;
                    """,
                    [submission_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No submission found with this ID."}
                return FormSubmissionOut(**record)
    
    def update_submission(self, submission_id: int, submission: FormSubmissionIn) -> Union[FormSubmissionOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE FormSubmissions
                    SET first_name = %s,
                        last_name = %s,
                        email = %s,
                        phone_number = %s,
                        teacher_status = %s,
                        cactus_number = %s,
                        guardian_name = %s,
                        classroom_size = %s,
                        number_of_classrooms = %s,
                        event_program_id = %s,
                        event_date_id = %s,
                        school_id = %s,
                        school_type_id = %s,
                        school_genre_id = %s,
                        grade_id = %s,
                        additional_contact = %s
                    WHERE submission_id = %s
                    RETURNING *;
                    """,
                    [
                        submission.first_name, submission.last_name, submission.email, 
                        submission.phone_number, submission.teacher_status, submission.cactus_number, submission.guardian_name, submission.classroom_size, 
                        submission.number_of_classrooms, submission.event_program_id, submission.event_date_id, 
                        submission.school_id, submission.school_type_id, submission.school_genre_id, 
                        submission.grade_id, submission.additional_contact, submission_id
                    ]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No submission found with this ID."}
                return FormSubmissionOut(**record)
    
    def delete_submission(self, submissionID: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM FormSubmissions
                    WHERE SubmissionID = %s
                    RETURNING *;
                    """,
                    [submissionID]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No submission found with this ID."}
                return {"message": "Submission deleted successfully"}
    
    def list_submissions(self) -> List[FormSubmissionOut]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT * FROM FormSubmissions;
                    """
                )
                records = db.fetchall()
                return [FormSubmissionOut(**record) for record in records]
