import './App.css';
import { AuthProvider } from './AuthContext';
import LoginPage from './loginForm';
import MainPage from './MainPage';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <div className='App'>
      <AuthProvider>
        <Router>
          <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/main" element={<MainPage />} />
            </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
