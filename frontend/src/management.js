import React, {useEffect, useState} from "react";
import { Container, Button, Fade, Form, Alert } from "react-bootstrap";
import { useAuth, useUserData } from './store/AuthContext';
import { useNavigate } from "react-router-dom";
import './CSS/MainPage.css';
import NavbarComponent from './Nav';
import { backendURL } from "./IPaddress";
import SchoolGenreComponent from "./crudFiles/schoolGenre";
import SchoolTypeComponent from "./crudFiles/schoolType";
import DistrictComponent from "./crudFiles/districts";
import SchoolComponent from "./crudFiles/schools";
import GradeComponent from "./crudFiles/grades";
import TeacherStatusComponent from "./crudFiles/teacherStatus";
import LocationComponent from "./crudFiles/locations";
import UserTypeComponent from "./crudFiles/appUserTypes";
import NewAccountForm from "./crudFiles/appUser";
import ClassroomComponent from "./crudFiles/classroom";
import ClassroomComp from "./crudFiles/classroomComp";

function Management() {
    const {authState, userType } = useAuth();
    const { userData } = useUserData();
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [upSchoolLoadStatus, setSchoolUploadStatus] = useState(null);
    const [upDistrictLoadStatus, setDistrictUploadStatus] = useState(null);
    const [ bulkLoad, setBulkLoad] = useState(false);
    // const [userType, setUserType] = useState('');
    const [showSchool, setShowSchool] = useState(false);
    const [showDistrict, setShowDistrict] = useState(false);
    const [showSchoolType, setShowSchoolType] = useState(false);
    const [showSchoolGenre, setShowSchoolGenre] = useState(false);
    const [showGrade, setShowGrade] = useState(false);
    const [showTeacherStatus, setShowTeacherStatus] = useState(false);
    const [showLocation, setShowLocation] = useState(false);
    const [showUserType, setShowUserType] = useState(false);
    const [showNewAccountForm, setShowNewAccountForm] = useState(false);
    const [showClassroom, setShowClassroom] = useState(false);


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
    const checkingUserID = () => {
        if (!userData.type_id) {
            console.log("the type is undefined: ", userData)
        } else {
            console.log("The type is: ", userData.type_id)
        }
    }
// this useEffect is to check for authentication. 
    useEffect(() => {
        if (!authState) {
            navigate('/login');
        }
    }, [authState, navigate]);

    useEffect(() => {
        // checkingUserID();
    }, []);

    // useEffect(() => {
    //     const fetchUserType = await fetch()
    // })

    // const renderContentBasedOnTypeId = () => {
    //     switch (userData.type_id) {
    //         case 5:
    //             // Access to levels 5, 4, 3, 2, 1
    //             return (

    //             );
    //         case 4:
    //             // Access to levels 4, 3, 2, 1
    //             return (
    //                 <>
    //                     <div>Level 4 Access Content</div>
    //                     {/* Fall through to include content for lower levels */}
    //                 </>
    //             );
    //         case 3:
    //             // Access to levels 3, 2, 1
    //             return (
    //                 <>
    //                     <div>Level 3 Access Content</div>
    //                     {/* Fall through to include content for lower levels */}
    //                 </>
    //             );
    //         case 2:
    //             // Access to level 2 and 1
    //             return (
    //                 <>
    //                     <div>Level 2 Access Content</div>
    //                     {/* Fall through to include content for lower levels */}
    //                 </>
    //             );
    //         case 1:
    //             // Access to level 1
    //             return <div>Level 1 Access Content</div>;
    //         default:
    //             // Default case if none of the above matches
    //             return <div>No Access</div>;
    //     }
    // };

    const renderContentBasedOnTypeId = () => {
        
 // I will need to use the text name of the user_type to determine what to add to the "content" list for displaying the components. 
        let content = [];

        switch (userData.type_id) {
            case 5:
                content.push(<div key="level5">                    <>
                <div>Level 5 Access Content</div>
                {/* Fall through to include content for lower levels */}
                    {/* Toggle Button for Bulk Load */}
                <Button className="d-flex" onClick={toggleBulkLoad}>
                    {bulkLoad ? "Hide Bulk Load Options" : "Show Bulk Load Options (schools and districts)"}
                </Button>
                <div>
                {/*file uploads */}
                {bulkLoad && (
                <Container className="vh-100 d-flex align-items-center justify-content-center">
                    
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
                </Container>)}
                </div>
            </></div>);
                // Fall through to level 4
            case 4:
                content.push(<div key="level4"><div>Level 4 Access Content</div><div>Working here</div></div>);
                // Fall through to level 3
            case 3:
                content.push(<div key="level3">Level 3 Access Content</div>);
                // Fall through to level 2
            case 2:
                content.push(<div key="level2">Level 2 Access Content</div>);
                // Fall through to level 1
            case 1:
                content.push(<div key="level1">Level 1 Access Content</div>);
                break;
            default:
                content.push(<div key="no-access">No Access</div>);
                break;
        }

        return content;
    };


    const toggleBulkLoad = () => {
        setBulkLoad(prevBulkLoad => !prevBulkLoad);
    };

    const onSchoolFileChange = (e) => {
        setFile(e.target.files[0]);
    };
    const onDistrictFileChange = (e) => {
        setFile(e.target.files[0]);
    };
    const toggleButtonStyle = (isShown) => isShown ? "danger" : "primary";
    const toggleButtonText = (isShown, text) => isShown ? `Hide ${text}` : `Expand ${text}`;
  
    



    return (
<div>
    <NavbarComponent/>
    {/* Below are the OBC CRUD operations */}
    
    { authState ? (
      <div>
      <Button variant={toggleButtonStyle(showSchool)} onClick={() => setShowSchool(!showSchool)} className="m-1">
        {toggleButtonText(showSchool, "School")}
      </Button>
      <Button variant={toggleButtonStyle(showDistrict)} onClick={() => setShowDistrict(!showDistrict)} className="m-1">
        {toggleButtonText(showDistrict, "District")}
      </Button>
      <Button variant={toggleButtonStyle(showSchoolType)} onClick={() => setShowSchoolType(!showSchoolType)} className="m-1">
        {toggleButtonText(showSchoolType, "School Type")}
      </Button>
      <Button variant={toggleButtonStyle(showSchoolGenre)} onClick={() => setShowSchoolGenre(!showSchoolGenre)} className="m-1">
        {toggleButtonText(showSchoolGenre, "School Genre")}
      </Button>
      <Button variant={toggleButtonStyle(showGrade)} onClick={() => setShowGrade(!showGrade)} className="m-1">
        {toggleButtonText(showGrade, "Grade")}
      </Button>
      <Button variant={toggleButtonStyle(showTeacherStatus)} onClick={() => setShowTeacherStatus(!showTeacherStatus)} className="m-1">
        {toggleButtonText(showTeacherStatus, "Teacher Status")}
      </Button>
      <Button variant={toggleButtonStyle(showLocation)} onClick={() => setShowLocation(!showLocation)} className="m-1">
        {toggleButtonText(showLocation, "Location")}
      </Button>
      <Button variant={toggleButtonStyle(showUserType)} onClick={() => setShowUserType(!showUserType)} className="m-1">
        {toggleButtonText(showUserType, "User Type")}
      </Button>
      <Button variant={toggleButtonStyle(showNewAccountForm)} onClick={() => setShowNewAccountForm(!showNewAccountForm)} className="m-1">
        {toggleButtonText(showNewAccountForm, "New Account Form")}
      </Button>
      <Button variant={toggleButtonStyle(showClassroom)} onClick={() => setShowClassroom(!showClassroom)} className="m-1">
        {toggleButtonText(showClassroom, "Classroom")}
      </Button>
        {showDistrict && <DistrictComponent />}
        {showSchool && <SchoolComponent />}
        {showSchoolType && <SchoolTypeComponent />}
        {showSchoolGenre && <SchoolGenreComponent />}
        {showGrade && <GradeComponent />}
        {showTeacherStatus && <TeacherStatusComponent />}
        {showLocation && <LocationComponent />}
        {showUserType && <UserTypeComponent />}
        {showNewAccountForm && <NewAccountForm />}
        {showClassroom && <ClassroomComponent />}

    </div>) : (<div><h1>Please refresh the page and login!</h1></div>)}

    {/*Checking Auth and loading the component*/}
        {/* {authState && (renderContentBasedOnTypeId())} */}
</div>

    );
}

export default Management;
