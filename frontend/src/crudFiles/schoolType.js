import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';

const SchoolTypeComponent = () => {
  const [types, setTypes] = useState([]);
  const [currentType, setCurrentType] = useState({ type: '', description: '' });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [typeToDelete, setTypeToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all types
  useEffect(() => {
    fetchTypes();
  }, []);

  const fetchTypes = async () => {
    const response = await fetch(`${backendURL}/api/schooltypes`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setTypes(data);
  };

  const handleFormChange = (e) => {
    setCurrentType({ ...currentType, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentType.type_id) {
      await updateType(currentType.type_id, currentType);
    } else {
      await createType(currentType);
    }
    setCurrentType({ type: '', description: '' });
    setShowForm(false);
    fetchTypes();
  };

  const createType = async (typeData) => {
    await fetch(`${backendURL}/api/schooltypes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(typeData),
      credentials: 'include'
    });
  };

  const updateType = async (typeId, typeData) => {
    await fetch(`${backendURL}/api/schooltypes/${typeId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(typeData),
      credentials: 'include'
    });
  };

  const deleteType = async () => {
    if (typeToDelete) {
      await fetch(`${backendURL}/api/schooltypes/${typeToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setTypeToDelete(null);
      setShowModal(false);
      fetchTypes();
    }
  };

  const editType = (type) => {
    setCurrentType(type);
    setShowForm(true);
  };
  const handleCancel = () => {
    setCurrentType({/*setting back to initial state */})
    setShowForm(false);
  }

  return (
    <div>
      <Button onClick={() => setShowForm(!showForm)} className="m-1">
        {showForm ? 'Show Types List' : 'Add New Type'}
      </Button>
  
      {showForm ? (
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="type">
            <Form.Label>Type</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter type"
              name="type"
              onChange={handleFormChange}
              value={currentType.type}
            />
          </Form.Group>
          <Form.Group controlId="description">
            <Form.Label>Description</Form.Label>
            <Form.Control 
              as="textarea"
              placeholder="Enter description"
              name="description"
              onChange={handleFormChange}
              value={currentType.description}
            />
          </Form.Group>
          <Button type="submit" className="m-1">Submit</Button>
          <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
        </Form>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>School Type</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {types.map((type) => (
              <tr key={type.type_id}>
                <td>{type.type}</td>
                <td>{type.description}</td>
                <td>
                  <Button onClick={() => editType(type)} className="m-1">Edit</Button>
                  <Button onClick={() => {
                    setTypeToDelete(type.type_id);
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
        <Modal.Body>Are you sure you want to delete this type?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteType}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default SchoolTypeComponent;
