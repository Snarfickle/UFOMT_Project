import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';

const GradeComponent = () => {
  const [grades, setGrades] = useState([]);
  const [currentGrade, setCurrentGrade] = useState({ grade: '', description: '' });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [gradeToDelete, setGradeToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all grades
  useEffect(() => {
    fetchGrades();
  }, []);

  const fetchGrades = async () => {
    const response = await fetch(`${backendURL}/api/grades`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setGrades(data);
  };

  const handleFormChange = (e) => {
    setCurrentGrade({ ...currentGrade, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentGrade.grade_id) {
      await updateGrade(currentGrade.grade_id, currentGrade);
    } else {
      await createGrade(currentGrade);
    }
    setCurrentGrade({ grade: '', description: '' });
    setShowForm(false);
    fetchGrades();
  };

  const createGrade = async (gradeData) => {
    await fetch(`${backendURL}/api/grades`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(gradeData),
      credentials: 'include'
    });
  };

  const updateGrade = async (gradeId, gradeData) => {
    await fetch(`${backendURL}/api/grades/${gradeId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(gradeData),
      credentials: 'include'
    });
  };

  const deleteGrade = async () => {
    if (gradeToDelete) {
      await fetch(`${backendURL}/api/grades/${gradeToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setGradeToDelete(null);
      setShowModal(false);
      fetchGrades();
    }
  };

  const editGrade = (grade) => {
    setCurrentGrade(grade);
    setShowForm(true);
  };

  const handleCancel = () => {
    setCurrentGrade({/*setting back to initial state */})
    setShowForm(false);
  }

  return (
    <div>
      <Button onClick={() => setShowForm(!showForm)} className="m-1">
        {showForm ? 'Show Grades List' : 'Add New Grade'}
      </Button>
  
      {showForm ? (
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="grade">
            <Form.Label>Grade</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter grade"
              name="grade"
              onChange={handleFormChange}
              value={currentGrade.grade}
            />
          </Form.Group>
          <Form.Group controlId="description">
            <Form.Label>Description</Form.Label>
            <Form.Control 
              as="textarea"
              placeholder="Enter description"
              name="description"
              onChange={handleFormChange}
              value={currentGrade.description}
            />
          </Form.Group>
          <Button type="submit" className="m-1">Submit</Button>
          <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
        </Form>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Grade</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {grades.map((grade) => (
              <tr key={grade.grade_id}>
                <td>{grade.grade}</td>
                <td>{grade.description}</td>
                <td>
                  <Button onClick={() => editGrade(grade)} className="m-1">Edit</Button>
                  <Button onClick={() => {
                    setGradeToDelete(grade.grade_id);
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
        <Modal.Body>Are you sure you want to delete this grade?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteGrade}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default GradeComponent;
