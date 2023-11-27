import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';

const UserTypeComponent = () => {
  const [userTypes, setUserTypes] = useState([]);
  const [currentUserType, setCurrentUserType] = useState({ type: '', description: '' });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [userTypeToDelete, setUserTypeToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all user types
  useEffect(() => {
    fetchUserTypes();
  }, []);

  const fetchUserTypes = async () => {
    const response = await fetch(`${backendURL}/api/usertypes`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setUserTypes(data);
  };

  const handleFormChange = (e) => {
    setCurrentUserType({ ...currentUserType, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentUserType.type_id) {
      await updateUserType(currentUserType.type_id, currentUserType);
    } else {
      await createUserType(currentUserType);
    }
    setCurrentUserType({ type: '', description: '' });
    setShowForm(false);
    fetchUserTypes();
  };

  const createUserType = async (userTypeData) => {
    await fetch(`${backendURL}/api/usertypes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userTypeData),
      credentials: 'include'
    });
  };

  const updateUserType = async (typeId, userTypeData) => {
    await fetch(`${backendURL}/api/usertypes/${typeId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userTypeData),
      credentials: 'include'
    });
  };

  const deleteUserType = async () => {
    if (userTypeToDelete) {
      await fetch(`${backendURL}/api/usertypes/${userTypeToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setUserTypeToDelete(null);
      setShowModal(false);
      fetchUserTypes();
    }
  };

  const editUserType = (userType) => {
    setCurrentUserType(userType);
    setShowForm(true);
  };

  const handleCancel = () => {
    setCurrentUserType({/*setting back to initial state */})
    setShowForm(false);
  }

return (
    <div>
      <Button onClick={() => setShowForm(!showForm)} className="m-1">
        {showForm ? 'Show User Types List' : 'Add New User Type'}
      </Button>
  
      {showForm ? (
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="type">
            <Form.Label>User Type</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter user type"
              name="type"
              onChange={handleFormChange}
              value={currentUserType.type}
            />
          </Form.Group>
          <Form.Group controlId="description">
            <Form.Label>Description</Form.Label>
            <Form.Control 
              as="textarea"
              placeholder="Enter description"
              name="description"
              onChange={handleFormChange}
              value={currentUserType.description}
            />
          </Form.Group>
          <Button type="submit" className="m-1">Submit</Button>
          <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>

        </Form>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Type</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {userTypes.map((type) => (
              <tr key={type.type_id}>
                <td>{type.type}</td>
                <td>{type.description}</td>
                <td>
                  <Button onClick={() => editUserType(type)} className="m-1">Edit</Button>
                  <Button onClick={() => {
                    setUserTypeToDelete(type.type_id);
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
        <Modal.Body>Are you sure you want to delete this user type?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteUserType}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
  
};

export default UserTypeComponent;
