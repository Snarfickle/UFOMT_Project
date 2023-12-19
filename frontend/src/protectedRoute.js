import React, { useContext, useEffect, useState } from 'react';
import { Navigate, Outlet, resolvePath, useNavigate } from 'react-router-dom';
import AuthContext from "./store/AuthContext";
import { backendURL } from './IPaddress';

const ProtectedRoute = () => {
    const { authState, setAuthState, checkAuth } = useContext(AuthContext);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();


    useEffect(() => {
        const checkAuthState = async () => {
            // console.log("protected route ran!")
            try {
                await checkAuth();
            } catch (error) {
                console.error('Error checking auth state:', error);
                setIsLoading(false);
            } finally {
                setIsLoading(false);
            }
        };

        if (!authState) {
            checkAuthState();
        } else {
            setIsLoading(false);  // If already authenticated, no need to check
        }
    }, [authState, setAuthState, navigate]);

    if (isLoading) {
        return <div>Loading...</div>; // Show loading while checking auth state
    }

    //return authState ? <Outlet /> : <Navigate to="/login" replace />; // Render child routes if authenticated
    return <Outlet />;
};

export default ProtectedRoute;
