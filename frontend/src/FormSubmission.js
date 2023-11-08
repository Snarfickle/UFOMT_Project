import React, { useState, useEffect, useMemo } from 'react';
import Select from 'react-select';
import { Form, Button, Alert, Modal } from 'react-bootstrap';
import './CSS/FormSubmission.css';
import { backendURL } from './IPaddress';
// for Private we need the form to say "private school students do not qualify for the 
// free POPS funding provided by this program. Please reach out to the UFOMT box office for a 50% off student discount"

// for homeschool, they also need to reach out to pam (email) for free dress rehersal tickets. 
// will be told NO for college, community, preschool,
// Only k-12 public school students and certified public school teachers qualify for the POPS funding provided by this program
const FormSubmission = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        guardian_name: '',
        teacher_status: false,
        cactus_number: '',
        school_id: '',
        district: '',
        event_program_id: '',
        event_date_id: '',
        grade_id: ''
    });
    const [loading, setLoading] = useState({
      grades: false,
      schools: false,
      eventPrograms: false,
      eventDates: false
  });
  const [error, setError] = useState({
      grades: null,
      schools: null,
      eventPrograms: null,
      eventDates: null
  });
    
    const [grades, setGrades] = useState([]);
    const [schools, setSchools] = useState([]);
    const [districts, setDistricts] = useState([]);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedSchool, setSelectedSchool] = useState(null);
    const [eventPrograms, setEventPrograms] = useState([]);
    const [eventDates, setEventDates] = useState([]);
    const [selectedEventProgram, setSelectedEventProgram] = useState(null);
    const [homeSchoolModal, setHomeSchoolModal] = useState(false);
    const [privateSchoolModal, setPrivateSchoolModal] = useState(false);
    const [disableSubmit, setDisableSubmit] = useState(false);
    const [ineligibleGradeModal, setIneligibleGradeModal] = useState(false);


    // Fetch data from APIs
    useEffect(() => {
      const fetchGrades = async () => {
        const url = `${backendURL}/api/grades`
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();

          if (Array.isArray(data)) {
            setGrades(data);
        } else {
            console.error('Fetched grades data is not an array:', data);

        }}
      };
      const fetchDistricts = async () => {
        const url = `${backendURL}/api/districts`;
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();
          setDistricts(data);
        }
      }

      const fetchSchools = async () => {
        setLoading(prev => ({ ...prev, schools: true }));
        const response = await fetch(`${backendURL}/api/schools`);
        
        if (!response.ok) throw new Error('Failed to fetch schools.');
        const data = await response.json();
        
        if (Array.isArray(data)) {
          setSchools(data);
      } else {
          console.error('Fetched Schools data is not an array:', data);

      }}

      const fetchEventPrograms = async () => {
          try {
              setLoading(prev => ({ ...prev, eventPrograms: true }));
              const response = await fetch(`${backendURL}/api/events-programs`);
              if (!response.ok) throw new Error('Failed to fetch event programs.');
              const data = await response.json();
              setEventPrograms(data);
          } catch (err) {
              setError(prev => ({ ...prev, eventPrograms: err.message }));
          } finally {
              setLoading(prev => ({ ...prev, eventPrograms: false }));
          }
      };

      const fetchEventDates = async () => {
        try {
            const response = await fetch(`${backendURL}/api/event-dates`);
            if (!response.ok) throw new Error('Failed to fetch event dates.');
            const data = await response.json();
            setEventDates(data);
            // console.log("dates: ", data)
        } catch (err) {
            console.error(err.message);
        }
      };

      fetchGrades();
      fetchSchools();
      fetchDistricts();
      fetchEventPrograms();
      fetchEventDates();
  }, []);

    const schoolOptions = schools.map(school_id => {
      const district = districts.find(d => d.district_id === school_id.district_id);
      const districtName = district ? district.name : 'Unknown District';
      
      return {
        label: `${school_id.name} (${districtName})`,
        value: school_id.school_id
      };
    });

    const relevantEventDates = useMemo(() => {
      if (!selectedEventProgram) return [];

      return eventDates
        .filter(event_date_id => event_date_id.event_id === Number(selectedEventProgram.value))
        .map(event_date_id => {
          return {
            label: `${event_date_id.date} ${event_date_id.start_time}`,
            value: event_date_id.event_dates_id
          };
        });
    }, [eventDates, selectedEventProgram]);
    

    const handleEventProgramChange = selectedOption => {
      setSelectedEventProgram(selectedOption);
      setFormData({
        ...formData,
        event_program_id: selectedOption ? parseInt(selectedOption.value, 10) : null,
        event_date_id: null  // resetting event date when event program changes
    });
    };

    const handleEventDateChange = (selectedOption) => {
      setFormData({
          ...formData,
          event_date_id: selectedOption ? selectedOption.value : null
      });
  };  

  const handleSchoolChange = selectedOption => {
        setSelectedSchool(selectedOption);
        let schoolId = null;
        if (selectedOption) {
            schoolId = parseInt(selectedOption.value, 10);
        if (isNaN(schoolId)) {
            console.warn(`Warning: could not parse school_id value "${selectedOption.value}" as an integer`);
            schoolId = null;
            }}
            setFormData({
            ...formData,
            school_id: schoolId
            });

            const selectedSchoolObj = schools.find(school_id => school_id.school_id === schoolId);
        if (selectedOption && selectedOption.label.includes("(Private)")) {
            setPrivateSchoolModal(true);
            setDisableSubmit(true);
            // Optionally, you may clear the form and selections here
            setFormData({
                first_name: '',
                last_name: '',
                email: '',
                phone_number: '',
                teacher_status: false,
                cactus_number: '',
                school_id: '',
                district: '',
                event_program_id: '',
                event_date_id: '',
                grade_id: ''
            });
            setSelectedSchool(null);
            setSelectedEventProgram(null);} 
        else if (selectedSchoolObj && selectedSchoolObj.name === "Home-School") {
            setHomeSchoolModal(true);
            setDisableSubmit(true);
            setFormData({
                first_name: '',
                last_name: '',
                email: '',
                phone_number: '',
                teacher_status: false,
                cactus_number: '',
                school_id: '',
                district: '',
                event_program_id: '',
                event_date_id: '',
                grade_id: ''
            });
            setSelectedSchool(null);
            setSelectedEventProgram(null);
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
            setFormData(prevFormData => ({
                ...prevFormData,
                district: correspondingDistrict.district_id
            }));
        }
      }
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
            
            // Optionally, you may clear the form and selections here
            setFormData({
                first_name: '',
                last_name: '',
                email: '',
                phone_number: '',
                teacher_status: false,
                cactus_number: '',
                school_id: '',
                district: '',
                event_program_id: '',
                event_date_id: '',
                grade_id: ''
            });
            setSelectedSchool(null);
            setSelectedEventProgram(null);
            
        } else {
            setDisableSubmit(false);
            setFormData({
                ...formData,
                grade_id: gradeValue
            });
        } 
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
          // Post formData to API
          const response = await fetch(`${backendURL}/api/form-submissions`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(formData)
          });
          // Check if post was successful
          if (!response.ok) {
              throw new Error('Network response was not ok:', Error);
          }
  
          // Log success and clear form
          setFormData({
              first_name: '',
              last_name: '',
              email: '',
              phone_number: '',
              teacher_status: false,
              cactus_number: '',
              school_id: '',
              district: '',
              event_program_id: '',
              event_date_id: '',
              grade_id: ''
          });
          setSelectedSchool(null);
          setSelectedEventProgram(null);
          // [Add other state reset actions as needed]
          
      } catch (error) {
          // Log error and potentially inform the user
          console.error('Failed to submit form:', error);
      }
  };
  
    return (
        <div  className='center-form'>
        <Form onSubmit={handleSubmit} className="my-form">
        {error.grades && <Alert variant="danger">{error.grades}</Alert>}
        {error.schools && <Alert variant="danger">{error.schools}</Alert>}
        {error.eventPrograms  && <Alert variant="danger">{error.eventPrograms }</Alert>}
        {error.eventDates  && <Alert variant="danger">{error.eventDates }</Alert>}

            <Form.Group controlId="first_name">
                <Form.Label className="bold-label">First Name</Form.Label>
                <Form.Control 
                    type="text"
                    placeholder="Enter first name"
                    name="first_name"
                    onChange={handleChange}
                    value={formData.first_name}
                />
            </Form.Group>

            <Form.Group controlId="last_name">
                <Form.Label className="bold-label">Last Name</Form.Label>
                <Form.Control 
                    type="text"
                    placeholder="Enter last name"
                    name="last_name"
                    onChange={handleChange}
                    value={formData.last_name}
                />
            </Form.Group>
            <Form.Group controlId="email">
                <Form.Label className="bold-label">Email</Form.Label>
                <Form.Control 
                    type="text"
                    placeholder="Enter Email"
                    name="email"
                    onChange={handleChange}
                    autoComplete='email'
                    value={formData.email}
                />
            </Form.Group>
            <Form.Group controlId="phone_number">
                <Form.Label className="bold-label">Phone number</Form.Label>
                <Form.Control 
                    type="text"
                    placeholder="Enter Phone number"
                    name="phone_number"
                    onChange={handleChange}
                    value={formData.phone_number}
                />
            </Form.Group>
            <Form.Group controlId="isTeacher">
            <Form.Label className="bold-label">Are you a Teacher?</Form.Label>
            <Form.Check 
                type="checkbox"
                label="Yes"
                name="teacher_status"
                checked={formData.teacher_status}
                onChange={e => handleChange({target: {name: e.target.name, value: e.target.checked}})}
            />
            </Form.Group>

            {formData.teacher_status ? (
                <Form.Group controlId="cactus_number">
                    <Form.Label className="bold-label">Cactus Number</Form.Label>
                    <Form.Control 
                        type="text"
                        placeholder="Enter Cactus Number"
                        name="cactus_number"
                        value={formData.cactus_number}
                        onChange={handleChange}
                    />
                </Form.Group>
            ) : (
                <Form.Group controlId="guardian_name">
                    <Form.Label className="bold-label">Guardian's Name</Form.Label>
                    <Form.Control 
                        type="text"
                        placeholder="Enter Guardian's Name"
                        name="guardian_name"
                        value={formData.guardian_name || ''}
                        onChange={handleChange}
                    />
                </Form.Group>
            )}

            <Form.Group controlId="grade_id">
                <Form.Label className="bold-label">Grade</Form.Label>
                <Form.Control 
                    as="select"
                    name="grade_id"
                    onChange={handleGradeChange}
                    value={formData.grade_id}
                >
                    <option value="">Select Grade</option>
                    {Array.isArray(grades) && grades.map(grade => (
                        <option key={grade.grade_id} value={grade.grade_id}>{grade.grade}</option>
                    ))}
                </Form.Control>
            </Form.Group>
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
            <Form.Group controlId="event_program_id">
                <Form.Label className="bold-label">Event Program</Form.Label>
                <Form.Control 
                  as="select"
                  name="event_program_id"
                  value={formData.event_program_id}
                  onChange={e => handleEventProgramChange({ value: e.target.value, label: e.target.options[e.target.selectedIndex].text })}
                >
                  <option value="">Select Event Program</option>
                  {eventPrograms.map(program => (
                    <option key={program.id} value={program.event_id}>{program.name}</option>
                  ))}
                </Form.Control>
            </Form.Group>

            <Form.Group controlId="event_date_id">
                <Form.Label className="bold-label">Event Date</Form.Label>
                <Select 
                    options={relevantEventDates}
                    onChange={handleEventDateChange}
                    value={relevantEventDates.find(date => date.value === formData.event_date_id) || null}
                    placeholder="Select Event Date"
                    isDisabled={!selectedEventProgram}
                    inputId="event_date_id"
                />
            </Form.Group>

            <Button type="submit" 
              disabled={
              !formData.first_name || !formData.last_name
              || !formData.email || !formData.phone_number
              || !formData.grade_id || !formData.event_program_id
              || !formData.event_date_id || disableSubmit
              }>
                Submit
            </Button>
        </Form>
            <Modal show={homeSchoolModal} onHide={() => setHomeSchoolModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Important Information</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Home-schooled students do not qualify for the free POPS funding provided by this program. Please reach out to Pamela Gee at "pamgee@ufomt.org" for a 50% student discount or for free dress rehearsal tickets
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setHomeSchoolModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
            <Modal show={privateSchoolModal} onHide={() => setPrivateSchoolModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Important Information</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Private school students do not qualify for the free POPS funding provided by this program. Please reach out to the UFOMT box office for a 50% off student discount
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setPrivateSchoolModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
            <Modal show={ineligibleGradeModal} onHide={() => setIneligibleGradeModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Important Information</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Only k-12 public school students and certified public school teachers qualify for the POPS funding provided by this program.
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setIneligibleGradeModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
    </div>
    );
};

export default FormSubmission;
