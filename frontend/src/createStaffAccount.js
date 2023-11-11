import React, { useEffect, useState } from 'react';
import { json, useNavigate } from "react-router-dom";
import { Form, Alert, Button, Modal } from 'react-bootstrap';
import Select from 'react-select';
import NavbarComponent from './Nav';
import { useAuth } from "./AuthContext";
import { backendURL } from './IPaddress';
import { AuthProvider } from './AuthContext';

function NewAccountForm() {
  const [formData, setFormData] = useState({
    username: '', 
    password: '',
    // confirmPassword: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    street: '',
    city: '',
    state: '',
    zip: '',
    employee_id: '',
    type_id: ''
  });
  const [passwordError, setPasswordError] = useState('');
  const {token} = useAuth();
  const [confirmPassword, setConfirmPassword] = useState('');
  const [userTypes, setUserTypes] = useState([]);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [submittedData, setSubmittedData ] = useState({});

  useEffect (() => {
    const fetchType_id = async () => {
        const url = `${backendURL}/api/usertypes`;
        const response = await fetch(url, {
            method: 'GET', 
            headers: {
                'Authorization':`Bearer ${token}`
            }
        })
        if (response.ok) {
            const data = await response.json();
            setUserTypes(data);
        } else {
            console.error("the fetch at user type_id failed");
        }
    }
    fetchType_id();
  },
  []);


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: value
    }));

    // If either the password or confirmPassword fields are updated,
    // clear the password error message.
    if (name === 'password' || name === 'confirmPassword') {
      setPasswordError('');
    }
  };

  const handlePasswordChange = (e) => {
    handleChange(e); // This updates the state for the password or confirmPassword

    // Check if passwords match only if the confirmPassword has been entered.
    if (confirmPassword && e.target.name === 'password') {
      if (e.target.value !== confirmPassword) {
        setPasswordError('Passwords do not match');
      } else {
        setPasswordError('');
      }
    }
  };
  const handleConfirmPasswordChange = (e) => {
    const value = e.target.value;
    setConfirmPassword(value);

    // Check if passwords match only if the password has been entered.
    if (formData.password) {
      if (formData.password !== e.target.value) {
        setPasswordError('Passwords do not match');
      } else {
        setPasswordError('');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Handle the form submission logic here, such as sending the data to a server
    const preparedFormData = {
        ...formData,
        type_id: parseInt(formData.type_id, 10),
        phone_number: parseInt(formData.phone_number, 10),
        zip: parseInt(formData.zip, 10)

    };
    try {
        const response = await fetch(`${backendURL}/api/admin-users`, {
            method: 'POST',
            headers: {
                'Authorization':`Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(preparedFormData)
        });
        if (response.ok) {
            setSubmittedData(preparedFormData);
            setSubmitSuccess(true);
            // Reset the form to initial state if needed
            setFormData({
              username: '', 
              password: '',
              confirmPassword: '',
              first_name: '',
              last_name: '',
              email: '',
              phone_number: '',
              street: '',
              city: '',
              state: '',
              zip: '',
              employee_id: '',
              type_id: '' // Assuming this is the correct initial state for type_id
            });
            setConfirmPassword('');
          } else {
            // Handle HTTP errors if the response is not ok
            const errorData = await response.json();
            alert(errorData.detail);
            console.error("Server responded with status", response.status);
          }
        } catch (error) {
          console.error("Failed to create new user", error);
        }
  };

  return (
    <div className="center-form">
    <NavbarComponent/>
    <div>
        <h2>Creating new staff account</h2>
    </div>

      <Form onSubmit={handleSubmit} className="my-form">
        <Form.Group controlId="username">
          <Form.Label className="bold-label">Username</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter a username"
              name="username"
              onChange={handleChange}
              value={formData.username}
          />
        </Form.Group>
        
        <Form.Group controlId="first_name">
          <Form.Label className="bold-label">First Name</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter first name"
              name="first_name"
              onChange={handleChange}
              value={formData.first_name}
          />
        </Form.Group>

        <Form.Group controlId="last_name">
          <Form.Label className="bold-label">Last Name</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter last name"
              name="last_name"
              onChange={handleChange}
              value={formData.last_name}
          />
        </Form.Group>

        <Form.Group controlId="email">
          <Form.Label className="bold-label">Email</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter Email"
              name="email"
              onChange={handleChange}
              autoComplete='email'
              value={formData.email}
          />
        </Form.Group>

        <Form.Group controlId="phone_number">
          <Form.Label className="bold-label">Phone number</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter Phone number"
              name="phone_number"
              onChange={handleChange}
              value={formData.phone_number}
          />
        </Form.Group>
        <Form.Group controlId="street">
          <Form.Label className="bold-label">Street</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter Street"
              name="street"
              onChange={handleChange}
              value={formData.street}
          />
        </Form.Group>
        <Form.Group controlId="city">
          <Form.Label className="bold-label">City</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter City"
              name="city"
              onChange={handleChange}
              value={formData.city}
          />
        </Form.Group>
        <Form.Group controlId="state">
          <Form.Label className="bold-label">State</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter State"
              name="state"
              onChange={handleChange}
              value={formData.state}
          />
        </Form.Group>
        <Form.Group controlId="zip">
          <Form.Label className="bold-label">Zip</Form.Label>
          <Form.Control 
              type="text"
              placeholder="Enter Zip"
              name="zip"
              onChange={handleChange}
              value={formData.zip}
          />
        </Form.Group>
        <Form.Group controlId="type_id">
          <Form.Label className="bold-label">Staff Type</Form.Label>
          <Form.Control 
              as="select"
            //   placeholder="Select User Type"
              name="type_id"
              onChange={handleChange}
              value={formData.type_id}
          >
            <option value="">Select Staff Type</option>
            {Array.isArray(userTypes) && userTypes.map(type_id => (
                <option key={type_id.type_id} value={type_id.type_id}>{type_id.type}</option>
            ))}
          </Form.Control>
        </Form.Group> 
        <Form.Group controlId="employee_id">
          <Form.Label className="bold-label">employee_id</Form.Label>
          <Form.Control 
              type="text"
              placeholder="employee_id"
              name="employee_id"
              onChange={handleChange}
              value={formData.employee_id}
          />
        </Form.Group> 
        <Form.Group controlId="password">
          <Form.Label className="bold-label">Password</Form.Label>
          <Form.Control 
              type="password"
              placeholder="Enter Password"
              name="password"
              onChange={handlePasswordChange}
              value={formData.password}
          />
        </Form.Group>      
        <Form.Group controlId="confirmPassword">
          <Form.Label className="bold-label">Confirm Password</Form.Label>
          <Form.Control 
              type="password"
              placeholder="Confirm Password"
              name="confirmPassword"
              onChange={handleConfirmPasswordChange}
              value={confirmPassword}
          />
          {passwordError && <div className="password-error">{passwordError}</div>}
        </Form.Group>

        <Button type="submit">
                  Submit
        </Button>
      </Form>
            <Modal show={submitSuccess} onHide={() => setSubmitSuccess(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>User created!</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Username: {submittedData.username} First and Last Name: {submittedData.first_name} {submittedData.last_name} Email: {submittedData.email} Staff Type: {submittedData.type_id} </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setSubmitSuccess(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
    </div>
  );
}

export default NewAccountForm;
