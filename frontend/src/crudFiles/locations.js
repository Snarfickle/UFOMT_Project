import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { backendURL } from '../IPaddress';

const LocationComponent = () => {
  const [locations, setLocations] = useState([]);
  const [currentLocation, setCurrentLocation] = useState({
    name: '', 
    seat_number: '', 
    address: '', 
    city: '', 
    state: '', 
    zip: '', 
    location_description: ''
  });
  const [showForm, setShowForm] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [locationToDelete, setLocationToDelete] = useState(null);
  const { authState } = useAuth();
  const navigate = useNavigate();

  // Authentication check
  useEffect(() => {
    if (!authState) {
        navigate('/login');
    }
  }, [authState, navigate]);

  // Fetch all locations
  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    const response = await fetch(`${backendURL}/api/locations`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await response.json();
    setLocations(data);
  };

  const handleFormChange = (e) => {
    setCurrentLocation({ ...currentLocation, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentLocation.location_id) {
      await updateLocation(currentLocation.location_id, currentLocation);
    } else {
      await createLocation(currentLocation);
    }
    setCurrentLocation({
      name: '', 
      seat_number: '', 
      address: '', 
      city: '', 
      state: '', 
      zip: '', 
      location_description: ''
    });
    setShowForm(false);
    fetchLocations();
  };

  const createLocation = async (locationData) => {
    await fetch(`${backendURL}/api/locations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(locationData),
      credentials: 'include'
    });
  };

  const updateLocation = async (locationId, locationData) => {
    await fetch(`${backendURL}/api/locations/${locationId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(locationData),
      credentials: 'include'
    });
  };

  const deleteLocation = async () => {
    if (locationToDelete) {
      await fetch(`${backendURL}/api/locations/${locationToDelete}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setLocationToDelete(null);
      setShowModal(false);
      fetchLocations();
    }
  };

  const editLocation = (location) => {
    setCurrentLocation(location);
    setShowForm(true);
  };

  const handleCancel = () => {
    setCurrentLocation({/*setting back to initial state */})
    setShowForm(false);
  }

return (
    <div>
      <Button onClick={() => setShowForm(!showForm)} className="m-1">
        {showForm ? 'Show Locations List' : 'Add New Location'}
      </Button>
  
      {showForm ? (
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="name">
            <Form.Label>Name</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter location name"
              name="name"
              onChange={handleFormChange}
              value={currentLocation.name}
            />
          </Form.Group>
          <Form.Group controlId="seat_number">
            <Form.Label>Number of Seats</Form.Label>
            <Form.Control 
              type="number"
              placeholder="Enter seat number"
              name="seat_number"
              onChange={handleFormChange}
              value={currentLocation.seat_number}
            />
          </Form.Group>
          <Form.Group controlId="address">
            <Form.Label>Address</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter address"
              name="address"
              onChange={handleFormChange}
              value={currentLocation.address}
            />
          </Form.Group>
          <Form.Group controlId="city">
            <Form.Label>City</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter city"
              name="city"
              onChange={handleFormChange}
              value={currentLocation.city}
            />
          </Form.Group>
          <Form.Group controlId="state">
            <Form.Label>State</Form.Label>
            <Form.Control 
              type="text"
              placeholder="Enter state"
              name="state"
              onChange={handleFormChange}
              value={currentLocation.state}
            />
          </Form.Group>
          <Form.Group controlId="zip">
            <Form.Label>Zip</Form.Label>
            <Form.Control 
              type="number"
              placeholder="Enter zip code"
              name="zip"
              onChange={handleFormChange}
              value={currentLocation.zip}
            />
          </Form.Group>
          <Form.Group controlId="location_description">
            <Form.Label>Location Description</Form.Label>
            <Form.Control 
              as="textarea"
              placeholder="Enter location description"
              name="location_description"
              onChange={handleFormChange}
              value={currentLocation.location_description}
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
              <th>Number of Seats</th>
              <th>Address</th>
              <th>City</th>
              <th>State</th>
              <th>Zip</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {locations.map((location) => (
              <tr key={location.location_id}>
                <td>{location.name}</td>
                <td>{location.seat_number}</td>
                <td>{location.address}</td>
                <td>{location.city}</td>
                <td>{location.state}</td>
                <td>{location.zip}</td>
                <td>{location.location_description}</td>
                <td>
                  <Button onClick={() => editLocation(location)} className="m-1">Edit</Button>
                  <Button variant="danger" onClick={() => {
                    setLocationToDelete(location.location_id);
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
        <Modal.Body>Are you sure you want to delete this location?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={deleteLocation}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
  
};

export default LocationComponent;
