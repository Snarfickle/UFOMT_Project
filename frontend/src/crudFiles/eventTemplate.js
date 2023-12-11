import React, { useState, useEffect } from 'react';
import { Modal, Form, Table, Button } from 'react-bootstrap';
import { useAuth } from '../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { backendURL } from '../IPaddress';

const EventTemplateComponent = () => {
    const [eventTemplates, setEventTemplates] = useState([]);
    const [currentEventTemplate, setCurrentEventTemplate] = useState({ name: '', location_id: '', description: '' });
    const [showForm, setShowForm] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [templateToDelete, setTemplateToDelete] = useState(null);
    const { authState } = useAuth();
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState('');

    // Redirect to login if not authenticated
    useEffect(() => {
        if (!authState) {
            navigate('/login');
        }
    }, [authState, navigate]);

    // Fetch all event templates
    useEffect(() => {
        fetchEventTemplates();
    }, []);

    const fetchEventTemplates = async () => {
        const response = await fetch(`${backendURL}/api/event-templates`, {
            method: 'GET',
            credentials: 'include'
        });
        const data = await response.json();
        setEventTemplates(data);
    };

    const handleFormChange = (e) => {
        setCurrentEventTemplate({ ...currentEventTemplate, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (currentEventTemplate.template_id) {
            await updateEventTemplate(currentEventTemplate.template_id, currentEventTemplate);
        } else {
            await createEventTemplate(currentEventTemplate);
        }
        setCurrentEventTemplate({ name: '', location_id: '', description: '' });
        setShowForm(false);
        fetchEventTemplates();
    };

    const filteredEventTemplates = eventTemplates.filter(template => 
        template.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    

    const createEventTemplate = async (templateData) => {
        await fetch(`${backendURL}/api/event-templates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(templateData),
            credentials: 'include'
        });
    };

    const updateEventTemplate = async (templateId, templateData) => {
        await fetch(`${backendURL}/api/event-templates/${templateId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(templateData),
            credentials: 'include'
        });
    };

    const deleteEventTemplate = async () => {
        if (templateToDelete) {
            await fetch(`${backendURL}/api/event-templates/${templateToDelete}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            setTemplateToDelete(null);
            setShowModal(false);
            fetchEventTemplates();
        }
    };

    const editEventTemplate = (template) => {
        setCurrentEventTemplate(template);
        setShowForm(true);
    };

    const handleCancel = () => {
        setCurrentEventTemplate({ name: '', location_id: '', description: '' });
        setShowForm(false);
    };

    return (
        <div>
            <Button onClick={() => setShowForm(!showForm)} className="m-1">
                {showForm ? 'Show Event Templates List' : 'Add New Event Template'}
            </Button>
            <Form.Group controlId="search">
            <Form.Control
                type="text"
                placeholder="Search by name..."
                onChange={(e) => setSearchQuery(e.target.value)}
            />
            </Form.Group>
            {showForm ? (
                <Form onSubmit={handleSubmit}>
                    <Form.Group controlId="name">
                        <Form.Label>Name</Form.Label>
                        <Form.Control 
                            type="text"
                            placeholder="Enter event template name"
                            name="name"
                            onChange={handleFormChange}
                            value={currentEventTemplate.name}
                        />
                    </Form.Group>
                    <Form.Group controlId="location_id">
                        <Form.Label>Location ID</Form.Label>
                        <Form.Control 
                            type="number"
                            placeholder="Enter location ID"
                            name="location_id"
                            onChange={handleFormChange}
                            value={currentEventTemplate.location_id}
                        />
                    </Form.Group>
                    <Form.Group controlId="description">
                        <Form.Label>Description</Form.Label>
                        <Form.Control 
                            as="textarea"
                            placeholder="Enter event template description"
                            name="description"
                            onChange={handleFormChange}
                            value={currentEventTemplate.description}
                        />
                    </Form.Group>
                    <Button type="submit" className="m-1">Submit</Button>
                    <Button variant="secondary" onClick={handleCancel} className="ml-2">Cancel</Button>
                </Form>
            ) : (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Location ID</th>
                            <th>Description</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredEventTemplates.map((template) => (
                            <tr key={template.template_id}>
                                <td>{template.name}</td>
                                <td>{template.location_id}</td>
                                <td>{template.description}</td>
                                <td>
                                    <Button onClick={() => editEventTemplate(template)} className="m-1">Edit</Button>
                                    <Button variant="danger" onClick={() => {
                                        setTemplateToDelete(template.template_id);
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
                <Modal.Body>Are you sure you want to delete this event template?</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Close
                    </Button>
                    <Button variant="danger" onClick={deleteEventTemplate}>
                        Delete
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
    

};

export default EventTemplateComponent;
