import React, {useEffect, useState} from "react";
import { Container, Button, Fade, Form, Alert } from "react-bootstrap";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";
import './CSS/MainPage.css';
import NavbarComponent from './Nav';
import { backendURL } from "./IPaddress";

function MainPage() {
    const [show, setShow] = useState(true);
    const {username, token, setToken, setUserName} = useAuth();
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [upSchoolLoadStatus, setSchoolUploadStatus] = useState(null);
    const [upDistrictLoadStatus, setDistrictUploadStatus] = useState(null);
    const [formSubCount, setFormSubCount] = useState();

    const onSchoolUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);
        
    // so make the file upload work, I had to remove the try & catch function while attempting the file upload.
    // The first attempt does what it can, and then removing the catch error seems to allow the omitted schools
    // to be entered. 
        try { 
            const response = await fetch(`${backendURL}/api/uploadschools`, {
                method: 'POST',
                body: formData,
                // headers: { 'Content-Type': 'multipart/form-data' } 
                // Note: Don't set Content-Type header when using FormData with Fetch
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok' + response.statusText);
            }
            
            setSchoolUploadStatus('Upload successful!');
        } catch (error) {
            console.error('Upload failed:', error);
            setSchoolUploadStatus('Upload failed. Please try again later.');
        }
    };
    const onDistrictUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            const response = await fetch(`${backendURL}/api/uploaddistricts`, {
                method: 'POST',
                body: formData,
                // headers: { 'Content-Type': 'multipart/form-data' } 
                // Note: Don't set Content-Type header when using FormData with Fetch
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok' + response.statusText);
            }
            
            setDistrictUploadStatus('Upload successful!');
        } catch (error) {
            console.error('Upload failed:', error);
            setDistrictUploadStatus('Upload failed. Please try again later.');
        }
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            setShow(false);
        }, 3000);
    },[]);
    useEffect(() => {
        const fetchFormSubCount = async () => {
            console.log("setToken: ", token);
            const url = `${backendURL}/api/form-submissions`;
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization':`Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();

                console.log("Form submissions data: ", data);
            } else {
                console.error("The fetch at form-submissions failed.")
            };
        };

        fetchFormSubCount();
    }, []);

    const handleLogout = () => {
        setToken(null);
        setUserName(null);
        navigate('/login');
    };
    const onSchoolFileChange = (e) => {
        setFile(e.target.files[0]);
    };
    const onDistrictFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    return (
<div>
    <NavbarComponent/>

    <Container className="vh-100 d-flex align-items-center justify-content-center">
        
        {/* Greeting Section */}
        <Fade in={show} timeout={4000}>
            <h1>Hello, {username}!</h1>
        </Fade>

        {/* School File Upload Section */}
        <Form>
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Upload your Schools CSV file second</Form.Label>
                <Form.Control 
                    type="file" 
                    onChange={onSchoolFileChange} 
                />
            </Form.Group>
            <Button onClick={onSchoolUpload}>Upload Schools</Button>
        </Form>
        
        {/* School Upload Status Message */}
        {upSchoolLoadStatus && (
            <Alert 
                variant={upSchoolLoadStatus.includes('successful') ? 'success' : 'danger'} 
                className="mt-3"
            >
                {upSchoolLoadStatus}
            </Alert>
        )}

        {/* District File Upload Section */}
        <Form>
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Upload your districts CSV file first</Form.Label>
                <Form.Control 
                    type="file" 
                    onChange={onDistrictFileChange} 
                />
            </Form.Group>
            <Button onClick={onDistrictUpload}>Upload Districts</Button>
        </Form>

        {/* District Upload Status Message */}
        {upDistrictLoadStatus && (
            <Alert 
                variant={upDistrictLoadStatus.includes('successful') ? 'success' : 'danger'} 
                className="mt-3"
            >
                {upDistrictLoadStatus}
            </Alert>
        )}
    </Container>
</div>

    );
}

export default MainPage;
