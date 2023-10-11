import './CSS/App.css';
import { AuthProvider } from './AuthContext';
import LoginPage from './loginForm';
import MainPage from './MainPage';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import FormSubmission from './FormSubmission';

function App() {
  return (
    <div className='App'>
      <AuthProvider>
        <Router>
          <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/main" element={<MainPage />} />
              <Route path="/formsubmission" element={<FormSubmission />} />
            </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
