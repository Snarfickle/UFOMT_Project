import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthContext'; // Ensure this hook provides your auth status

function ProtectedRoute() {
  let { token } = useAuth(); 

  return token ? <Outlet /> : <Navigate to="/login" />;
}

export default ProtectedRoute
