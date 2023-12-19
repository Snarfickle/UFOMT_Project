import React, { useState, useEffect } from 'react';
import { Modal, Form, Table, Button } from 'react-bootstrap';
import { backendURL } from '../IPaddress';
import { useAuth } from '../store/AuthContext';
import { useNavigate } from 'react-router-dom';


const SchoolGenreComponent = () => {
    const [genres, setGenres] = useState([]);
    const [currentGenre, setCurrentGenre] = useState({ type: '', description: '' });
    const [showForm, setShowForm] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [genreToDelete, setGenreToDelete] = useState(null);
    const { authState } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
    // Dependency array includes authState to react to its changes
    }, [authState, navigate]);

    // Fetch all genres
    useEffect(() => {
        fetchGenres();
    }, []);


    const fetchGenres = async () => {
        const response = await fetch(`${backendURL}/api/schoolgenres`, {
        method: 'GET',
        credentials: 'include'
        });
        const data = await response.json();
        setGenres(data);
    };

    const handleFormChange = (e) => {
        setCurrentGenre({ ...currentGenre, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (currentGenre.genre_id) {
        await updateGenre(currentGenre.genre_id, currentGenre);
        } else {
        await createGenre(currentGenre);
        }
        setCurrentGenre({ type: '', description: '' });
        setShowForm(false);
        fetchGenres();
    };

    const createGenre = async (genreData) => {
        await fetch(`${backendURL}/api/schoolgenres`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(genreData),
        credentials: 'include'
        });
    };

    const updateGenre = async (genreId, genreData) => {
        await fetch(`${backendURL}/api/schoolgenres/${genreId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(genreData),
        credentials: 'include'
        });
    };

    const deleteGenre = async () => {
        if (genreToDelete) {
          await fetch(`${backendURL}/api/schoolgenres/${genreToDelete}`, {
            method: 'DELETE',
            credentials: 'include'
          });
          setGenreToDelete(null);
          setShowModal(false);
          fetchGenres();
        }
    };

    const editGenre = (genre) => {
        setCurrentGenre(genre);
        setShowForm(true);
    };

    const handleCancel = () => {
        setCurrentGenre({/*setting back to initial state */})
        setShowForm(false);
      }

    return (
        <div>
        <Button onClick={() => setShowForm(!showForm)} className="m-1">
            {showForm ? 'Show Genres List' : 'Add New Genre'}
        </Button>
        {showForm ? (
            <Form onSubmit={handleSubmit}>
            <Form.Group controlId="type">
                <Form.Label>Type</Form.Label>
                <Form.Control 
                type="text"
                placeholder="Enter genre type"
                name="type"
                onChange={handleFormChange}
                value={currentGenre.type}
                />
            </Form.Group>
            <Form.Group controlId="description">
                <Form.Label>Description</Form.Label>
                <Form.Control 
                as="textarea"
                placeholder="Enter genre description"
                name="description"
                onChange={handleFormChange}
                value={currentGenre.description}
                />
            </Form.Group>
            <Button type="submit" className="m-1">Submit</Button>
            <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
            </Form>
        ) : (
            <Table striped bordered hover>
            <thead>
                <tr>
                <th>School Genre</th>
                <th>Description</th>
                <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {genres.map((genre) => (
                <tr key={genre.genre_id}>
                    <td>{genre.type}</td>
                    <td>{genre.description}</td>
                    <td>
                    <Button onClick={() => editGenre(genre)} className="m-1">Edit</Button>
                    <Button variant="danger" onClick={() => {
                        setGenreToDelete(genre.genre_id);
                        setShowModal(true);
                    }}>Delete</Button>
                    </td>
                </tr>
                ))}
            </tbody>
            </Table>
        )}
        <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete this genre?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteGenre}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
        </div>
    );
};

export default SchoolGenreComponent;
