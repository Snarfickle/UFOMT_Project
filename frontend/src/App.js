import './CSS/App.css';
import { AuthProvider } from './AuthContext';
import LoginPage from './loginForm';
import MainPage from './MainPage';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import FormSubmission from './FormSubmission';
import ProtectedRoute from './protectedRoute';
import NewAccountForm from './createStaffAccount';


function App() {
  return (
    <div className='App'>
      <AuthProvider>
        <Router>
          <Routes>
              <Route path="login" element={<LoginPage />} />
              <Route path="main" element={<ProtectedRoute />}>
                <Route index element={<MainPage />} />
              </Route>
              <Route path="/new-account" element={<ProtectedRoute />}>
              <Route index element={<NewAccountForm />} />
              </Route>
              <Route path="*" element={<Navigate to="/main" replace />} />
              <Route path="/formsubmission" element={<FormSubmission />} />
            </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
