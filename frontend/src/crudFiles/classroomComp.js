import React, { useState, useEffect, useMemo } from 'react';
import { Modal, Button, Form, Table, Dropdown } from 'react-bootstrap';
import Select from 'react-select';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';
import '../CSS/classroom.css';

const initialClassroomState = {
    size: '', 
    grade_id: '', 
    teacher_id: '', 
    drama_mentor_id: '', 
    art_mentor_id: '', 
    music_mentor_id: '',
    school_id: ''
  };
  
  const initialTeacherSearchState = {
    teacherSearch: "",
    selectedTeacherName: ''
  };
  
  const initialMentorSearchState = {
    dramaMentorSearch: "",
    artMentorSearch: "",
    musicMentorSearch: "",
    selectedDramaMentorName: '',
    selectedArtMentorName: '',
    selectedMusicMentorName: ''
  };
  
  const initialModalStates = {
    ineligibleGradeModal: false,
    disableSubmit: false,
    homeSchoolModal: false,
    privateSchoolModal: false
  };

const ClassroomComp = () => {
  const [classrooms, setClassrooms] = useState([]);
  const [currentClassroom, setCurrentClassroom] = useState(initialClassroomState);
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [classroomToDelete, setClassroomToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();

  const [mentors, setMentors] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [grades, setGrades] = useState([]);
  const [schools, setSchools] = useState([]);
  const [districts, setDistricts] = useState([]);

  const [selectedSchool, setSelectedSchool] = useState(null);
  const [selectedDistrict, setSelectedDistrict] = useState(null);

  const [teacherSearchDetails, setTeacherSearchDetails] = useState(initialTeacherSearchState);
  const [mentorSearchDetails, setMentorSearchDetails] = useState(initialMentorSearchState);

  const [modalStates, setModalStates] = useState(initialModalStates);

    // Authentication check and data fetching
    useEffect(() => {
        if (!authState) navigate('/login');
        fetchData();
      }, []);
    
      const fetchData = async () => {
        await Promise.all([
          fetchClassrooms(),
          fetchUsers(),
          fetchGrades(),
          fetchSchools(),
          fetchDistricts()
        ]);
      };
    // Fetch classrooms
    const fetchClassrooms = async () => {
    try {
      const response = await fetch(`${backendURL}/api/classrooms`, {
        method: 'GET',
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Failed to fetch classrooms.');
      const data = await response.json();
      setClassrooms(data);
    } catch (error) {
      console.error('Error fetching classrooms:', error);
    }
  };

  // Fetch users (teachers and mentors)
  const fetchUsers = async () => {
    try {
      const response = await fetch(`${backendURL}/api/app-users`, {
        method: 'GET',
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Failed to fetch users.');
      const data = await response.json();
      const teachers = data.filter(user => user.type_id === 1);
      const mentors = data.filter(user => user.type_id === 3);
      setTeachers(teachers);
      setMentors(mentors);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  // Fetch grades
  const fetchGrades = async () => {
    try {
      const response = await fetch(`${backendURL}/api/grades`, {
        method: 'GET',
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Failed to fetch grades.');
      const data = await response.json();
      setGrades(data);
    } catch (error) {
      console.error('Error fetching grades:', error);
    }
  };

  // Fetch schools
  const fetchSchools = async () => {
    try {
      const response = await fetch(`${backendURL}/api/schools`, {
        method: 'GET',
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Failed to fetch schools.');
      const data = await response.json();
      setSchools(data);
    } catch (error) {
      console.error('Error fetching schools:', error);
    }
  };

  // Fetch districts
  const fetchDistricts = async () => {
    try {
      const response = await fetch(`${backendURL}/api/districts`, {
        method: 'GET',
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Failed to fetch districts.');
      const data = await response.json();
      setDistricts(data);
    } catch (error) {
      console.error('Error fetching districts:', error);
    }
  };

    // Handle changes in the school dropdown
    const handleSchoolChange = selectedOption => {
        setSelectedSchool(selectedOption);
        const schoolId = selectedOption ? parseInt(selectedOption.value, 10) : null;
        if (isNaN(schoolId)) {
          console.warn(`Warning: could not parse school_id value "${selectedOption.value}" as an integer`);
        }
    
        setCurrentClassroom(prev => ({ ...prev, school_id: schoolId }));
        handleSchoolSpecificModals(selectedOption, schoolId);
      };
    
      // Handle specific modal triggers based on school selection
      const handleSchoolSpecificModals = (selectedOption, schoolId) => {
        const selectedSchoolObj = schools.find(school => school.school_id === schoolId);
        // Logic for handling specific modals based on school type
        // Set modals and disable submit button as necessary
        // ...
      };
    
      // Handle changes in the mentor dropdowns
      const handleMentorSelect = (mentorId, mentorType, mentorName) => {
        setCurrentClassroom(prev => ({ ...prev, [`${mentorType}_id`]: mentorId }));
    
        // Set the name of the selected mentor based on mentorType
        // Update search state as necessary
        // ...
      };
    
      // Handle changes in the teacher dropdown
      const handleTeacherSelect = (teacherId, teacherName) => {
        setCurrentClassroom(prev => ({ ...prev, teacher_id: teacherId }));
        setTeacherSearchDetails({ teacherSearch: '', selectedTeacherName: teacherName });
      };
    
      // Handle form field changes
      const handleFormChange = (e) => {
        const { name, value } = e.target;
        setCurrentClassroom(prev => ({ ...prev, [name]: value }));
      };
    
      // Handle changes in the grade dropdown
      const handleGradeChange = e => {
        const gradeId = parseInt(e.target.value, 10);
        if (isNaN(gradeId)) {
          console.warn(`Warning: could not parse grade value "${e.target.value}" as an integer`);
        }
    
        setCurrentClassroom(prev => ({ ...prev, grade_id: gradeId }));
        // Handle any specific logic related to grade change
        // ...
      };
    
      // Handle submission of the classroom form
      const handleSubmit = async e => {
        e.preventDefault();
        const classroomId = currentClassroom.classroom_id;
        if (classroomId) {
          await updateClassroom(classroomId, currentClassroom);
        } else {
          await createClassroom(currentClassroom);
        }
        resetFormState();
        fetchClassrooms();
      };
    
      // Handle cancel action in the form
      const handleCancel = () => {
        resetFormState();
      };
    
      // Reset form state to initial values
      const resetFormState = () => {
        setCurrentClassroom(initialClassroomState);
        setTeacherSearchDetails(initialTeacherSearchState);
        setMentorSearchDetails(initialMentorSearchState);
        // Reset other states as necessary
      };
        // Utility function to create a new classroom
  const createClassroom = async (classroomData) => {
    try {
      const response = await fetch(`${backendURL}/api/classrooms`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(classroomData),
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Failed to create classroom.');
      // Handle success (e.g., show a success message, update state)
    } catch (error) {
      console.error('Error creating classroom:', error);
      // Handle error (e.g., show error message)
    }
  };

  // Utility function to update an existing classroom
  const updateClassroom = async (classroomId, classroomData) => {
    try {
      const response = await fetch(`${backendURL}/api/classrooms/${classroomId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(classroomData),
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Failed to update classroom.');
      // Handle success
    } catch (error) {
      console.error('Error updating classroom:', error);
      // Handle error
    }
  };

  // Utility function to delete a classroom
  const deleteClassroom = async () => {
    if (classroomToDelete) {
      try {
        const response = await fetch(`${backendURL}/api/classrooms/${classroomToDelete}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        if (!response.ok) throw new Error('Failed to delete classroom.');
        setClassroomToDelete(null);
        setShowModal(false);
        fetchClassrooms();
        // Handle additional success operations
      } catch (error) {
        console.error('Error deleting classroom:', error);
        // Handle error
      }
    }
  };

  // Utility function to filter teachers based on a search term
  const filterTeachers = (searchTerm) => {
    return teachers.filter(teacher =>
      `${teacher.first_name} ${teacher.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()));
  };

  // Utility function to filter mentors based on a search term
  const filterMentors = (searchTerm, mentorType) => {
    return mentors.filter(mentor =>
      mentor.type_id === mentorType && 
      `${mentor.first_name} ${mentor.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const ClassroomForm = ({ /* props */ }) => {
    // Form JSX using the passed props
    return <form> {/* Form elements here */}</form>;
  };
  const ClassroomsTable = ({ classrooms, editClassroom, setClassroomToDelete, setShowModal }) => {
    // JSX for displaying the classrooms in a table
    return (
      <table>
        {/* Table headers and rows using classrooms data */}
      </table>
    );
  };

  const editClassroom = (classroom) => {
    // Logic to edit the selected classroom
    setCurrentClassroom(classroom);
    // Any additional logic for editing a classroom
  };
  const DeleteConfirmationModal = ({ showModal, setShowModal, deleteClassroom }) => {
    // JSX for the modal
    return (
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        {/* Modal content */}
      </Modal>
    );
  };

  const schoolOptions = useMemo(() => {
    return schools.map(school => ({
      label: `${school.name} (additional details)`,
      value: school.id
    }));
  }, [schools]);

  return (
    <div>
      {/* Toggle form button */}
      <Button onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Show Classrooms List' : 'Add New Classroom'}
      </Button>
  
      {/* Conditional rendering of form or classrooms list */}
      {showForm ? (
        <ClassroomForm
          currentClassroom={currentClassroom}
          handleFormChange={handleFormChange}
          handleSchoolChange={handleSchoolChange}
          handleGradeChange={handleGradeChange}
          handleSubmit={handleSubmit}
          handleCancel={handleCancel}
          handleTeacherSelect={handleTeacherSelect}
          handleMentorSelect={handleMentorSelect}
          teacherSearchDetails={teacherSearchDetails}
          mentorSearchDetails={mentorSearchDetails}
          schools={schools}
          grades={grades}
          schoolOptions={schoolOptions} // Assuming schoolOptions is derived from schools state
          filterTeachers={filterTeachers}
          filterMentors={filterMentors}
          selectedSchool={selectedSchool}
        />
      ) : (
        <ClassroomsTable
          classrooms={classrooms}
          editClassroom={editClassroom}
          setClassroomToDelete={setClassroomToDelete}
          setShowModal={setShowModal}
        />
      )}

      {/* Delete Confirmation Modal */}
      <DeleteConfirmationModal
        showModal={showModal}
        setShowModal={setShowModal}
        deleteClassroom={deleteClassroom}
      />
    </div>
  );

};



export default ClassroomComp;
