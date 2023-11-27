import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table, Dropdown } from 'react-bootstrap';
import Select from 'react-select';
import { useAsyncError, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';
import '../CSS/classroom.css';

const ClassroomComponent = () => {
  const [classrooms, setClassrooms] = useState([]);
  const [currentClassroom, setCurrentClassroom] = useState({
    size: '', 
    grade_id: '', 
    teacher_id: '', 
    drama_mentor_id: '', 
    art_mentor_id: '', 
    music_mentor_id: '',
    school_id: ''
  });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [classroomToDelete, setClassroomToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();
  const [ mentors, setMentors ] = useState([]);
  const [ teachers, setTeachers ] = useState([]);
  const [teacherSearch, setTeacherSearch] = useState("");
  const [selectedTeacherName, setSelectedTeacherName] = useState('');
  const [dramaMentorSearch, setDramaMentorSearch] = useState("");
  const [artMentorSearch, setArtMentorSearch] = useState("");
  const [musicMentorSearch, setMusicMentorSearch] = useState("");
  const [selectedDramaMentorName, setSelectedDramaMentorName] = useState('');
  const [selectedArtMentorName, setSelectedArtMentorName] = useState('');
  const [selectedMusicMentorName, setSelectedMusicMentorName] = useState('');
  const [ grades, setGrades ] = useState([]);
  const [ineligibleGradeModal, setIneligibleGradeModal] = useState(false);
  const [disableSubmit, setDisableSubmit] = useState(false);
  const [ schools, setSchools] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [selectedSchool, setSelectedSchool] = useState(null);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [homeSchoolModal, setHomeSchoolModal] = useState(false);
  const [privateSchoolModal, setPrivateSchoolModal] = useState(false);

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all classrooms
  useEffect(() => {
    fetchClassrooms();
    fetchUsers();
    fetchGrades();
    fetchSchools();
    fetchDistricts();
  }, []);

  const fetchSchools = async () => {
    // setLoading(prev => ({ ...prev, schools: true }));
    const response = await fetch(`${backendURL}/api/schools`);
    
    if (!response.ok) throw new Error('Failed to fetch schools.');
    const data = await response.json();
    
    if (Array.isArray(data)) {
      setSchools(data);
  } else {
      console.error('Fetched Schools data is not an array:', data);

  }}
  const fetchDistricts = async () => {
    const url = `${backendURL}/api/districts`;
    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      setDistricts(data);
    }
  }

  const fetchClassrooms = async () => {
    const response = await fetch(`${backendURL}/api/classrooms`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setClassrooms(data);
  };

  const fetchGrades = async () => {
    const response = await fetch(`${backendURL}/api/grades`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setGrades(data);
  };

  const fetchUsers = async () => {
    const response = await fetch(`${backendURL}/api/app-users`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    const teachers = data.filter(user => user.type_id === 1)
    const mentors = data.filter(user => user.type_id === 3)
    setMentors(mentors);
    setTeachers(teachers);
  };

  const schoolOptions = schools.map(school_id => {
    const district = districts.find(d => d.district_id === school_id.district_id);
    const districtName = district ? district.name : 'Unknown District';
    
    return {
      label: `${school_id.name} (${districtName})`,
      value: school_id.school_id
    };
  });

  const handleSchoolChange = selectedOption => {
    setSelectedSchool(selectedOption);
    let schoolId = null;
    if (selectedOption) {
        schoolId = parseInt(selectedOption.value, 10);
    if (isNaN(schoolId)) {
        console.warn(`Warning: could not parse school_id value "${selectedOption.value}" as an integer`);
        schoolId = null;
        }}
        setCurrentClassroom({
        ...currentClassroom,
        school_id: schoolId
        });

        const selectedSchoolObj = schools.find(school_id => school_id.school_id === schoolId);
    if (selectedOption && selectedOption.label.includes("(Private)")) {
        setPrivateSchoolModal(true);
        setDisableSubmit(true);
        // Optionally, you may clear the form and selections here
        setCurrentClassroom({
            size: '', 
            grade_id: '', 
            teacher_id: '', 
            drama_mentor_id: '', 
            art_mentor_id: '', 
            music_mentor_id: '',
            school_id: ''
        });
        setSelectedSchool(null);} 
    else if (selectedSchoolObj && selectedSchoolObj.name === "Home-School") {
        setHomeSchoolModal(true);
        setDisableSubmit(true);
        setCurrentClassroom({
            size: '', 
            grade_id: '', 
            teacher_id: '', 
            drama_mentor_id: '', 
            art_mentor_id: '', 
            music_mentor_id: '',
            school_id: ''
        });
        setSelectedSchool(null);
    } else {
        setDisableSubmit(false);
    }

    if (selectedSchoolObj)  {
        // Find the corresponding district object
        const correspondingDistrict = districts.find(district => district.district_id === selectedSchoolObj.district_id);
    
    if (correspondingDistrict) {
        // Update the district in the state
        setSelectedDistrict(correspondingDistrict);

        // Update the district in the formData
        setCurrentClassroom(prevFormData => ({
            ...prevFormData,
            district: correspondingDistrict.district_id
        }));
    }
  }
};

  const handleMentorSelect = (mentorId, mentorType, mentorName) => {
    setCurrentClassroom({
      ...currentClassroom,
      [`${mentorType}_id`]: mentorId
    });

    // Update the name of the selected mentor
    if (mentorType === 'drama_mentor') {
        setSelectedDramaMentorName(mentorName);
        setDramaMentorSearch('');
    };
    if (mentorType === 'art_mentor') {
        setSelectedArtMentorName(mentorName);
        setArtMentorSearch('');
    };
    if (mentorType === 'music_mentor') {
        setSelectedMusicMentorName(mentorName);
        setMusicMentorSearch('');
    };
  };
  const handleTeacherSelect = (teacherId, teacherName) => {
    setCurrentClassroom({
      ...currentClassroom,
      teacher_id: teacherId
    });
    setSelectedTeacherName(teacherName);
    setTeacherSearch('');
    };
    const filterTeachers = (searchTerm) => {
        return teachers.filter(teacher =>
            `${teacher.first_name} ${teacher.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()))
    }

  const handleFormChange = (e) => {
    setCurrentClassroom({ ...currentClassroom, [e.target.name]: e.target.value });
  };

  const handleGradeChange = (e) => {
    const gradeValueStr = e.target.value;
    let gradeValue = parseInt(gradeValueStr, 10);
    
    // Check if the parsed value is NaN and handle accordingly
    if (isNaN(gradeValue)) {
        console.warn(`Warning: could not parse grade value "${gradeValueStr}" as an integer`);
        gradeValue = null; // or handle differently based on your use-case
    }
        // Find the selected grade object
        const selectedGrade = grades.find(grade => grade.grade_id === gradeValue);

    // Check if selected grade is one of the ineligible grades
    if (selectedGrade && ["College", "Community", "Preschool"].includes(selectedGrade.grade)) {
        setIneligibleGradeModal(true);
        setDisableSubmit(true);
        
        // setSelectedSchool(null);
        // setSelectedEventProgram(null);
        
    } else {
        setDisableSubmit(false);
        setCurrentClassroom({
            ...currentClassroom,
            grade_id: gradeValue
        });
    } 
};

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentClassroom.classroom_id) {
      await updateClassroom(currentClassroom.classroom_id, currentClassroom);
    } else {
      await createClassroom(currentClassroom);
    }
    setCurrentClassroom({
      size: '', 
      grade_id: '', 
      teacher_id: '', 
      drama_mentor_id: '', 
      art_mentor_id: '', 
      music_mentor_id: '',
      school_id: ''
    });
    setShowForm(false);
    fetchClassrooms();
  };

  const getGradeType = (gradeId) => {
    const grade = grades.find(g => g.grade_id === gradeId)
    if (grade) {
      return grade.grade
    }
    return "Unknown Grade";
  }

  const getTeacherName = (teacherId) => {
    const teacher = teachers.find(t => t.user_id === teacherId)
    if (teacher) {
      return `${teacher.first_name} ${teacher.last_name}`
    }
  }

  const getMentorName = (mentorId) => {
    const mentor = mentors.find(t => t.user_id === mentorId)
    if (mentor) {
      return `${mentor.first_name} ${mentor.last_name}`
    }
  }

  const filterMentors = (searchTerm) => {
    return mentors.filter(mentor =>
        `${mentor.first_name} ${mentor.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const createClassroom = async (classroomData) => {
    await fetch(`${backendURL}/api/classrooms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(classroomData),
      credentials: 'include'
    });
  };

  const updateClassroom = async (classroomId, classroomData) => {
    await fetch(`${backendURL}/api/classrooms/${classroomId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(classroomData),
      credentials: 'include'
    });
  };

  const deleteClassroom = async () => {
    if (classroomToDelete) {
      await fetch(`${backendURL}/api/classrooms/${classroomToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setClassroomToDelete(null);
      setShowModal(false);
      fetchClassrooms();
    }
  };

  const editClassroom = (classroom) => {
    // Set the current classroom state with the selected classroom data
    setCurrentClassroom({
      size: classroom.size,
      grade_id: classroom.grade_id,
      teacher_id: classroom.teacher_id,
      drama_mentor_id: classroom.drama_mentor_id,
      art_mentor_id: classroom.art_mentor_id,
      music_mentor_id: classroom.music_mentor_id,
      school_id: classroom.school_id
    });
    setSelectedArtMentorName()
  
    // Update other relevant states, if necessary. For example, if you have dropdowns or selectors in your form, 
    // you might need to set their states as well based on the classroom data
  
    // Show the form modal
    setShowForm(true);
  };

  const handleCancel = () => {
    setCurrentClassroom({/*setting back to initial state */})
    setShowForm(false);
    setCurrentClassroom({
        size: '', 
        grade_id: '', 
        teacher_id: '', 
        drama_mentor_id: '', 
        art_mentor_id: '', 
        music_mentor_id: ''
      });
    setDramaMentorSearch('');
    setArtMentorSearch('');
    setMusicMentorSearch('');
    setSelectedDramaMentorName('');
    setSelectedArtMentorName('');
    setSelectedMusicMentorName('');
    
  }

return (
    <div>
      <Button onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Show Classrooms List' : 'Add New Classroom'}
      </Button>
  
      {showForm ? (
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="school_id">
            <Form.Label className="bold-label">School</Form.Label>
            <Select 
                isSearchable={true}
                options={schoolOptions}
                value={selectedSchool}
                onChange={handleSchoolChange}
                inputId="school_id"
            />
        </Form.Group>
      <Form.Group controlId="size">
        <Form.Label>Size</Form.Label>
        <Form.Control
        type="text"
        name="size"
        value={currentClassroom.size}
        onChange={handleFormChange}
        />

      </Form.Group>

      <Form.Group controlId="grade_id">
                <Form.Label className="bold-label">Grade</Form.Label>
                <Form.Control 
                    as="select"
                    name="grade_id"
                    onChange={handleGradeChange}
                    value={currentClassroom.grade_id}
                >
                    <option value="">Select Grade</option>
                    {Array.isArray(grades) && grades.map(grade => (
                        <option key={grade.grade_id} value={grade.grade_id}>{grade.grade}</option>
                    ))}
                </Form.Control>
            </Form.Group>

          {/* Teacher Search and Display */}
          <Form.Group controlId="teacher_search">
            <Form.Label>Teacher</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Search teacher"
              value={teacherSearch}
              onChange={(e) => setTeacherSearch(e.target.value)}
            />
            <Dropdown className="mentor-search-dropdown">
              {teacherSearch && filterTeachers(teacherSearch).map(teacher => (
                <Dropdown.Item 
                  key={teacher.user_id} 
                  onClick={() => handleTeacherSelect(teacher.user_id, `${teacher.first_name} ${teacher.last_name}`)}
                >
                  {`${teacher.first_name} ${teacher.last_name}`}
                </Dropdown.Item>
              ))}
            </Dropdown>
            {selectedTeacherName && <div>Selected Teacher: {selectedTeacherName}</div>}
          </Form.Group>

          {/* Drama Mentor Search */}
          <Form.Group controlId="drama_mentor_search">
            <Form.Label>Drama Mentor</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Search drama mentor"
              value={dramaMentorSearch}
              onChange={(e) => setDramaMentorSearch(e.target.value)}
            />
            <Dropdown className="mentor-search-dropdown">
              {dramaMentorSearch && filterMentors(dramaMentorSearch).map(mentor => (
                <Dropdown.Item 
                  key={mentor.user_id} 
                  onClick={() => handleMentorSelect(mentor.user_id, 'drama_mentor', `${mentor.first_name} ${mentor.last_name}`)}
                >
                  {`${mentor.first_name} ${mentor.last_name}`}
                </Dropdown.Item>
              ))}
            </Dropdown>
            {selectedDramaMentorName && <div>Selected Mentor: {selectedDramaMentorName}</div>}
          </Form.Group>

          {/* Art Mentor Search and Display */}
          <Form.Group controlId="art_mentor_search">
            <Form.Label>Art Mentor</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Search art mentor"
              value={artMentorSearch}
              onChange={(e) => setArtMentorSearch(e.target.value)}
            />
            <Dropdown className="mentor-search-dropdown">
              {artMentorSearch && filterMentors(artMentorSearch).map(mentor => (
                <Dropdown.Item 
                  key={mentor.user_id} 
                  onClick={() => handleMentorSelect(mentor.user_id, 'art_mentor', `${mentor.first_name} ${mentor.last_name}`)}
                >
                  {mentor.first_name} {mentor.last_name}
                </Dropdown.Item>
              ))}
            </Dropdown>
            {selectedArtMentorName && <div>Selected Mentor: {selectedArtMentorName}</div>}
          </Form.Group>

          {/* Music Mentor Search and Display */}
          <Form.Group controlId="music_mentor_search">
            <Form.Label>Music Mentor</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Search music mentor"
              value={musicMentorSearch}
              onChange={(e) => setMusicMentorSearch(e.target.value)}
            />
            <Dropdown className="mentor-search-dropdown">
              {musicMentorSearch && filterMentors(musicMentorSearch).map(mentor => (
                <Dropdown.Item 
                  key={mentor.user_id} 
                  onClick={() => handleMentorSelect(mentor.user_id, 'music_mentor', `${mentor.first_name} ${mentor.last_name}`)}
                >
                  {mentor.first_name} {mentor.last_name}
                </Dropdown.Item>
              ))}
            </Dropdown>
            {selectedMusicMentorName && <div>Selected Mentor: {selectedMusicMentorName}</div>}
          </Form.Group>

          {/* Include additional form fields for grade_id, teacher_id, etc. */}
          {/* ... */}
          <Button type="submit" className="m-1">Submit</Button>
          <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
        </Form>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Classroom Size</th>
              <th>Grade</th>
              <th>Teacher</th>
              <th>Drama Mentor</th>
              <th>Art Mentor</th>
              <th>Music Mentor</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {classrooms.map((classroom) => (
              <tr key={classroom.classroom_id}>
                <td>{classroom.size}</td>
                <td>{getGradeType(classroom.grade_id)}</td>
                <td>{getTeacherName(classroom.teacher_id)}</td>
                <td>{getMentorName(classroom.drama_mentor_id)}</td>
                <td>{getMentorName(classroom.art_mentor_id)}</td>
                <td>{getMentorName(classroom.music_mentor_id)}</td>
                <td>
                  <Button className="m-1" onClick={() => editClassroom(classroom)}>Edit</Button>
                  <Button className="m-1" onClick={() => {
                    setClassroomToDelete(classroom.classroom_id);
                    setShowModal(true);
                  }}>Delete</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
  
      {/* Delete Confirmation Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete this classroom?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteClassroom}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}  
export default ClassroomComponent;
