import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table, Pagination, InputGroup, FormControl } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';

const SchoolComponent = () => {
  const [allSchools, setAllSchools] = useState([]);
  const [displayedSchools, setDisplayedSchools] = useState([]);
  const [currentSchool, setCurrentSchool] = useState({ /* initial school state */ });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [schoolToDelete, setSchoolToDelete] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const recordsPerPage = 10;
  const { authState } = useAuth();
  const [districts, setDistricts] = useState([]);
  const [types, setTypes] = useState([]);
  const [genres, setGenres] = useState([]);

  const navigate = useNavigate();

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all schools
  useEffect(() => {
    fetchSchools();
    fetchDistricts();
    fetchGenres();
    fetchTypes();
  }, []);

  const fetchTypes = async () => {
    const url = `${backendURL}/api/schooltypes`;
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include'
    });
    if (response.ok) {
      const data = await response.json();
      setTypes(data);
    }
  };
  const fetchGenres = async () => {
    const url = `${backendURL}/api/schoolgenres`;
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include'
    });
    if (response.ok) {
      const data = await response.json();
      setGenres(data);
    }
  };
  const fetchDistricts = async () => {
    const url = `${backendURL}/api/districts`;
    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      setDistricts(data);
    }
  }
  const getDistrictName = (schoolId) => {
    const school = allSchools.find(s => s.school_id === schoolId);
    if (school) {
      const district = districts.find(d => d.district_id === school.district_id);
      return district ? district.name : 'Unknown District';
    }
    return 'Unknown District';
  };

  const fetchSchools = async () => {
    try {
      const response = await fetch(`${backendURL}/api/schools`, {
        method: 'GET',
        credentials: 'include'
      });
      const data = await response.json();  
      // Check if the data contains the 'schools' property
      if (data) {
        setAllSchools(data);
        setTotalPages(Math.ceil(data.schools.length / recordsPerPage));
        updateDisplayedSchools(1, data.schools);
      } else {
        // Handle cases where 'schools' is not in the response
        console.error('Schools data is not available in the response');
        setAllSchools([]);
        setTotalPages(0);
        updateDisplayedSchools(1, []);
      }
    } catch (error) {
      console.error('Error fetching schools:', error);
      // Handle error scenario
    }
  };
  

  // Update displayed schools when page changes or data changes
  useEffect(() => {
    updateDisplayedSchools(currentPage, allSchools);
  }, [currentPage, allSchools]);


  const updateDisplayedSchools = (page, schools) => {
    // Ensure schools is defined and not null
    if (schools && schools.length > 0) {
      const startIndex = (page - 1) * recordsPerPage;
      const endIndex = startIndex + recordsPerPage;
      setDisplayedSchools(schools.slice(startIndex, endIndex));
    } else {
      // If schools is undefined or empty, set displayedSchools to an empty array
      setDisplayedSchools([]);
    }
  };

  const handleSearch = () => {
    // if the search term is greater than 0
    if (searchTerm.length > 0 ) {
    const filteredSchools = allSchools.filter(school => 
      school.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setTotalPages(Math.ceil(filteredSchools.length / recordsPerPage));
    updateDisplayedSchools(1, filteredSchools);
    setCurrentPage(1);
  } else { // else display the original data
    updateDisplayedSchools(1, allSchools);
    setTotalPages(0);
  };
  };

  const handleFormChange = (e) => {
    setCurrentSchool({ ...currentSchool, [e.target.name]: e.target.value });
  };

  const handleSearchChange = (e) => {
  setSearchTerm(e.target.value.toLowerCase());
  };

  const handleCreateNewSchool = () => {
    setCurrentSchool({ /* reset to initial state with empty fields */ });
    setShowForm(true);
  };  

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentSchool.school_id) {
      await updateSchool(currentSchool.school_id, currentSchool);
    } else {
      await createSchool(currentSchool);
    }
    setCurrentSchool({ /* reset to initial state */ });
    setShowForm(false);
    fetchSchools();
  };

  const createSchool = async (schoolData) => {
    try {
      const response = await fetch(`${backendURL}/api/schools`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(schoolData),
        credentials: 'include'
      });
      if (!response.ok) {
        throw new Error('Failed to create school.');
      }
      fetchSchools();
    } catch (error) {
      console.error('Error creating school:', error);
      // Optionally, handle the error in the UI
    }
  };

  const updateSchool = async (schoolId, schoolData) => {
    try {
      const response = await fetch(`${backendURL}/api/schools/${schoolId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(schoolData),
        credentials: 'include'
      });
      if (!response.ok) {
        throw new Error('Failed to update school.');
      }
      fetchSchools();
    } catch (error) {
      console.error('Error updating school:', error);
      // Optionally, handle the error in the UI
    }
  };

  const deleteSchool = async () => {
    try {
      const response = await fetch(`${backendURL}/api/schools/${schoolToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      if (!response.ok) {
        throw new Error('Failed to delete school.');
      }
      fetchSchools();
    } catch (error) {
      console.error('Error deleting school:', error);
      // Optionally, handle the error in the UI
    }
    setSchoolToDelete(null);
    setShowModal(false);    
  };

  const editSchool = (school) => {
    setCurrentSchool(school);
    setShowForm(true);
  };

  const handleCancel = () => {
    setCurrentSchool({/*setting back to initial state */})
    setShowForm(false);
  }

  // Pagination Controls
  const getPaginationItems = () => {
    let items = [];
    for (let number = 1; number <= totalPages; number++) {
      items.push(
        <Pagination.Item key={number} active={number === currentPage} onClick={() => setCurrentPage(number)}>
          {number}
        </Pagination.Item>
      );
    }
    return items;
  };

  return (
    <div>
      {/* "Create School" Button */}
      <Button variant="primary" onClick={handleCreateNewSchool} className="mb-3">Add New School</Button>
      <InputGroup className="mb-3">
        <FormControl
          placeholder="Search schools"
          onChange={handleSearchChange}
          value={searchTerm}
        />
        <Button onClick={handleSearch} className="m-1">Search</Button>
      </InputGroup>
      
      {showForm ? (
        <Form onSubmit={handleSubmit}>
          {/* School Name */}
          <Form.Group controlId="name">
            <Form.Label>School Name</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter school name"
              name="name"
              onChange={handleFormChange}
              value={currentSchool.name}
            />
          </Form.Group>

          {/* Phone */}
          <Form.Group controlId="phone">
            <Form.Label>Phone</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter phone number"
              name="phone"
              onChange={handleFormChange}
              value={currentSchool.phone}
            />
          </Form.Group>

          {/* Street */}
          <Form.Group controlId="street">
            <Form.Label>Street</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter street address"
              name="street"
              onChange={handleFormChange}
              value={currentSchool.street}
            />
          </Form.Group>

          {/* City */}
          <Form.Group controlId="city">
            <Form.Label>City</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter city"
              name="city"
              onChange={handleFormChange}
              value={currentSchool.city}
            />
          </Form.Group>

          {/* State */}
          <Form.Group controlId="state">
            <Form.Label>State</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter state"
              name="state"
              onChange={handleFormChange}
              value={currentSchool.state}
            />
          </Form.Group>

          {/* Zip Code */}
          <Form.Group controlId="zip">
            <Form.Label>Zip</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter zip code"
              name="zip"
              onChange={handleFormChange}
              value={currentSchool.zip}
            />
          </Form.Group>
        {/* Student Body Count */}
        <Form.Group controlId="student_body_count">
            <Form.Label>Student Body Count</Form.Label>
            <Form.Control 
              type="number"
              placeholder="Enter student body count"
              name="student_body_count"
              onChange={handleFormChange}
              value={currentSchool.student_body_count}
            />
          </Form.Group>
          {/* Title One Status */}
          <Form.Group controlId="title_one_status">
            <Form.Label>Title One Status</Form.Label>
            <Form.Check 
              type="checkbox"
              label="Title One School"
              name="title_one_status"
              onChange={e => handleFormChange({
                target: {
                  name: e.target.name,
                  value: e.target.checked
                }
              })}
              checked={currentSchool.title_one_status}
            />
          </Form.Group>
          {/* District ID */}
          <Form.Group controlId="district_id">
            <Form.Label>District</Form.Label>
            <Form.Control 
              as="select"
              name="district_id"
              onChange={handleFormChange}
              value={currentSchool.district_id}
            >
              <option value="">Select District</option>
              {districts.map(district => (
                <option key={district.district_id} value={district.district_id}>
                  {district.name}
                </option>
              ))}
            </Form.Control>
          </Form.Group>
          {/* Type ID - Assuming you have type data similar to districts */}
          <Form.Group controlId="type_id">
            <Form.Label>Type</Form.Label>
            <Form.Control 
              as="select"
              name="type_id"
              onChange={handleFormChange}
              value={currentSchool.type_id}
            >
              <option value="">Select Type</option>
              {types.map(type => (
                <option key={type.type_id} value={type.type_id}>{type.type}</option>
              ))}
            </Form.Control>
          </Form.Group>
          {/* Genre ID - Assuming you have genre data similar to districts */}
          <Form.Group controlId="genre_id">
            <Form.Label>Genre</Form.Label>
            <Form.Control 
              as="select"
              name="genre_id"
              onChange={handleFormChange}
              value={currentSchool.genre_id}
            >
              <option value="">Select Genre</option>
              {genres.map(genre => (
                <option key={genre.genre_id} value={genre.genre_id}>{genre.type}</option>
              ))}
            </Form.Control>
          </Form.Group>
          
          {/* Add other fields similarly */}
          <Button type="submit" className="m-1">Submit</Button>
          <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
        </Form>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th>Street</th>
              <th>State</th>
              <th>Zip</th>
              <th>Student Body Count</th>
              <th>Title One Status</th>
              <th>Type</th>
              <th>Genre</th>
              <th>District</th>
              {/* Other table headers */}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {displayedSchools.map((school) => (
              <tr key={school.school_id}>
                <td>{school.name}</td>
                <td>{school.phone}</td>
                <td>{school.street}</td>
                <td>{school.state}</td>
                <td>{school.zip}</td>
                <td>{school.student_body_count}</td>
                <td>{school.title_one_status}</td>
                <td>{school.type}</td>
                <td>{school.genre}</td>
                <td>{getDistrictName(school.school_id)}</td>
                {/* Other table columns */}
                <td>
                  <Button onClick={() => editSchool(school)} className="m-1">Edit</Button>
                  <Button variant="danger" onClick={() => {
                    setSchoolToDelete(school.school_id);
                    setShowModal(true);
                  }} className="m-1">Delete</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
      {/* Pagination */}
      <Pagination className="justify-content-center">
        {getPaginationItems()}
      </Pagination>

      {/* Delete Confirmation Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete this school?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteSchool}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default SchoolComponent;
