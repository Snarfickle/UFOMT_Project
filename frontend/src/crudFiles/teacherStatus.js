import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';

const TeacherStatusComponent = () => {
  const [statuses, setStatuses] = useState([]);
  const [currentStatus, setCurrentStatus] = useState({ status: '', description: '' });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [statusToDelete, setStatusToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all teacher statuses
  useEffect(() => {
    fetchTeacherStatuses();
  }, []);

  const fetchTeacherStatuses = async () => {
    const response = await fetch(`${backendURL}/api/teacherstatuses`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setStatuses(data);
  };

  const handleFormChange = (e) => {
    setCurrentStatus({ ...currentStatus, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentStatus.teacher_status_id) {
      await updateTeacherStatus(currentStatus.teacher_status_id, currentStatus);
    } else {
      await createTeacherStatus(currentStatus);
    }
    setCurrentStatus({ status: '', description: '' });
    setShowForm(false);
    fetchTeacherStatuses();
  };

  const createTeacherStatus = async (statusData) => {
    await fetch(`${backendURL}/api/teacherstatuses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(statusData),
      credentials: 'include'
    });
  };

  const updateTeacherStatus = async (statusId, statusData) => {
    await fetch(`${backendURL}/api/teacherstatuses/${statusId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(statusData),
      credentials: 'include'
    });
  };

  const deleteTeacherStatus = async () => {
    if (statusToDelete) {
      await fetch(`${backendURL}/api/teacherstatuses/${statusToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setStatusToDelete(null);
      setShowModal(false);
      fetchTeacherStatuses();
    }
  };

  const editTeacherStatus = (status) => {
    setCurrentStatus(status);
    setShowForm(true);
  };

  const handleCancel = () => {
    setCurrentStatus({/*setting back to initial state */})
    setShowForm(false);
  }

  return (
    <div>
      <Button onClick={() => setShowForm(!showForm)} className="m-1">
        {showForm ? 'Show Statuses List' : 'Add New Status'}
      </Button>
  
      {showForm ? (
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="status">
            <Form.Label>Status</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter status"
              name="status"
              onChange={handleFormChange}
              value={currentStatus.status}
            />
          </Form.Group>
          <Form.Group controlId="description">
            <Form.Label>Description</Form.Label>
            <Form.Control 
              as="textarea"
              placeholder="Enter description"
              name="description"
              onChange={handleFormChange}
              value={currentStatus.description}
            />
          </Form.Group>
          <Button type="submit" className="m-1">Submit</Button>
          <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
        </Form>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Status</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {statuses.map((status) => (
              <tr key={status.teacher_status_id}>
                <td>{status.status}</td>
                <td>{status.description}</td>
                <td>
                  <Button onClick={() => editTeacherStatus(status)} className="m-1">Edit</Button>
                  <Button onClick={() => {
                    setStatusToDelete(status.teacher_status_id);
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
        <Modal.Body>Are you sure you want to delete this status?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteTeacherStatus}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default TeacherStatusComponent;
