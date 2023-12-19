import React, { useState, useEffect } from 'react';
import { Modal, Form, Table, Button } from 'react-bootstrap';
import { useAuth } from '../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { backendURL } from '../IPaddress';

const EventTypeComponent = () => {
    const [eventTypes, setEventTypes] = useState([]);
    const [currentEventType, setCurrentEventType] = useState({ name: '', description: '' });
    const [showForm, setShowForm] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [eventTypeToDelete, setEventTypeToDelete] = useState(null);
    const { authState } = useAuth();
    const navigate = useNavigate();

    // Redirect to login if not authenticated
    useEffect(() => {
        if (!authState) {
            navigate('/login');
        }
    }, [authState, navigate]);

    // Fetch all event types
    useEffect(() => {
        fetchEventTypes();
    }, []);

    const fetchEventTypes = async () => {
        const response = await fetch(`${backendURL}/api/event-types`, {
            method: 'GET',
            credentials: 'include'
        });
        const data = await response.json();
        setEventTypes(data);
    };

    const handleFormChange = (e) => {
        setCurrentEventType({ ...currentEventType, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (currentEventType.event_type_id) {
            await updateEventType(currentEventType.event_type_id, currentEventType);
        } else {
            await createEventType(currentEventType);
        }
        setCurrentEventType({ name: '', description: '' });
        setShowForm(false);
        fetchEventTypes();
    };

    const createEventType = async (eventTypeData) => {
        await fetch(`${backendURL}/api/event-types`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(eventTypeData),
            credentials: 'include'
        });
    };

    const updateEventType = async (eventTypeId, eventTypeData) => {
        await fetch(`${backendURL}/api/event-types/${eventTypeId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(eventTypeData),
            credentials: 'include'
        });
    };

    const deleteEventType = async () => {
        if (eventTypeToDelete) {
            await fetch(`${backendURL}/api/event-types/${eventTypeToDelete}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            setEventTypeToDelete(null);
            setShowModal(false);
            fetchEventTypes();
        }
    };

    const editEventType = (eventType) => {
        setCurrentEventType(eventType);
        setShowForm(true);
    };

    const handleCancel = () => {
        setCurrentEventType({ name: '', description: '' });
        setShowForm(false);
    };
    return (
        <div>
            <Button onClick={() => setShowForm(!showForm)} className="m-1">
                {showForm ? 'Show Event Types List' : 'Add New Event Type'}
            </Button>
            {showForm ? (
                <Form onSubmit={handleSubmit}>
                    <Form.Group controlId="name">
                        <Form.Label>Name</Form.Label>
                        <Form.Control 
                            type="text"
                            placeholder="Enter event type name"
                            name="name"
                            onChange={handleFormChange}
                            value={currentEventType.name}
                        />
                    </Form.Group>
                    <Form.Group controlId="description">
                        <Form.Label>Description</Form.Label>
                        <Form.Control 
                            as="textarea"
                            placeholder="Enter event type description"
                            name="description"
                            onChange={handleFormChange}
                            value={currentEventType.description}
                        />
                    </Form.Group>
                    <Button type="submit" className="m-1">Submit</Button>
                    <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
                </Form>
            ) : (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Event Type Name</th>
                            <th>Description</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {eventTypes.map((eventType) => (
                            <tr key={eventType.event_type_id}>
                                <td>{eventType.name}</td>
                                <td>{eventType.description}</td>
                                <td>
                                    <Button onClick={() => editEventType(eventType)} className="m-1">Edit</Button>
                                    <Button variant="danger" onClick={() => {
                                        setEventTypeToDelete(eventType.event_type_id);
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
                <Modal.Body>Are you sure you want to delete this event type?</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Close
                    </Button>
                    <Button variant="danger" onClick={deleteEventType}>
                        Delete
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default EventTypeComponent;
