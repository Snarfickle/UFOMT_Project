import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';

const DistrictComponent = () => {
  const [districts, setDistricts] = useState([]);
  const [currentDistrict, setCurrentDistrict] = useState({ name: '', zipcode: '' });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [districtToDelete, setDistrictToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all districts
  useEffect(() => {
    fetchDistricts();
  }, []);

  const fetchDistricts = async () => {
    const response = await fetch(`${backendURL}/api/districts`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setDistricts(data);
  };

  const handleFormChange = (e) => {
    setCurrentDistrict({ ...currentDistrict, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentDistrict.district_id) {
      await updateDistrict(currentDistrict.district_id, currentDistrict);
    } else {
      await createDistrict(currentDistrict);
    }
    setCurrentDistrict({ name: '', zipcode: '' });
    setShowForm(false);
    fetchDistricts();
  };

  const createDistrict = async (districtData) => {
    await fetch(`${backendURL}/api/districts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(districtData),
      credentials: 'include'
    });
  };

  const updateDistrict = async (districtId, districtData) => {
    await fetch(`${backendURL}/api/districts/${districtId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(districtData),
      credentials: 'include'
    });
  };

  const deleteDistrict = async () => {
    if (districtToDelete) {
      await fetch(`${backendURL}/api/districts/${districtToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setDistrictToDelete(null);
      setShowModal(false);
      fetchDistricts();
    }
  };

  const editDistrict = (district) => {
    setCurrentDistrict(district);
    setShowForm(true);
  };

  const handleCancel = () => {
    setCurrentDistrict({/*setting back to initial state */})
    setShowForm(false);
  }

  return (
    <div>
      <Button onClick={() => setShowForm(!showForm)} className="m-1">
        {showForm ? 'Show Districts List' : 'Add New District'}
      </Button>

      {showForm ? (
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="name">
            <Form.Label>Name</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter district name"
              name="name"
              onChange={handleFormChange}
              value={currentDistrict.name}
            />
          </Form.Group>
          <Form.Group controlId="zipcode">
            <Form.Label>Zipcode</Form.Label>
            <Form.Control 
              type="number"
              placeholder="Enter zipcode"
              name="zipcode"
              onChange={handleFormChange}
              value={currentDistrict.zipcode}
            />
          </Form.Group>
          <Button type="submit" className="m-1">Submit</Button>
          <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
        </Form>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>District Name</th>
              <th>Zipcode</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {districts.map((district) => (
              <tr key={district.district_id}>
                <td>{district.name}</td>
                <td>{district.zipcode}</td>
                <td>
                  <Button onClick={() => editDistrict(district)} className="m-1">Edit</Button>
                  <Button onClick={() => {
                    setDistrictToDelete(district.district_id);
                    setShowModal(true);
                  }} className="m-1">Delete</Button>
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
        <Modal.Body>Are you sure you want to delete this district?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteDistrict}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default DistrictComponent;
