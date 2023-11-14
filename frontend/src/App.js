import './CSS/App.css';
import { AuthProvider } from './store/AuthContext';
import LoginPage from './loginForm';
import MainPage from './MainPage';
import { BrowserRouter as Router, Route, Routes, useNavigate, Navigate } from 'react-router-dom';
import FormSubmission from './FormSubmission';
import ProtectedRoute from './protectedRoute';
import NewAccountForm from './createStaffAccount';
import Management from './management';

function AppWithRouter() {
    const navigate = useNavigate();

    return (
        <div className='App'>
            <AuthProvider navigate={navigate}>
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route element={<ProtectedRoute />}>
                        <Route path="/main" element={<MainPage />} />
                        <Route path="/new-account" element={<NewAccountForm />} />
                        <Route path="/formsubmission" element={<FormSubmission />} />
                        <Route path="/management" element={<Management />} />

                        {/* You can add more protected routes here */}
                    </Route>
                    <Route path="*" element={<Navigate to="/main" replace />} />
                </Routes>
            </AuthProvider>
        </div>
    );
}
function App() {
    return (
        <Router>
            <AppWithRouter />
        </Router>
    );
}

export default App;
