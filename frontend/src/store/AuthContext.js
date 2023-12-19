import React, { createContext, useState, useContext, useEffect } from 'react';
import { backendURL } from '../IPaddress';

const AuthContext = createContext();
const UserDataContext = createContext();

export const useAuth = () => useContext(AuthContext);
export const useUserData = () => useContext(UserDataContext);

export const AuthProvider = ({ children, navigate }) => {
    const [authState, setAuthState] = useState(false);
    const [userData, setUserData] = useState(null);
    const [userId, setUserId] = useState(localStorage.getItem('userId') || '');
    const [userType, setUserType] = useState('');


    const login = async (user, password) => {
        
        const response = await fetch(`${backendURL}/api/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${user}&password=${encodeURIComponent(password)}`,
            credentials: 'include',
        });
        if (response.ok) {
            const data = await response.json();
            
            setAuthState(true);
            checkAuth();
            fetchUserInfo();
            fetchUserType();
            // Fetch user info right after setting the username
            // await fetchUserInfo();
            navigate('/main');
        } else{
            throw new Error("Username or password is incorrect!")
        }
    };

    const logout = async () => {
        
        await fetch(`${backendURL}/api/logout/`, {
            method: 'POST',
            credentials: 'include',
        });
        setAuthState(false);
        localStorage.removeItem('userId'); // Clear userId from localStorage
        setUserId('');
        navigate('/login');
    };

    const checkAuth = async () => {
        
        const response = await fetch(`${backendURL}/api/check-auth`, {
            method: 'GET',
            credentials: 'include',
        });
    
        if (response.ok) {
            try {
                const data = await response.json();
                setUserId(data);
                localStorage.setItem('userId', data); // Store userId in localStorage
                setAuthState(true);
            } catch (error) {
                console.error("Error reading response data:", error);
                // Handle any errors that occur during JSON parsing
            }
        } else {
            setAuthState(false);
            // navigate('/login');
        }
    };

    const fetchUserInfo = async () => {
        
        // 
        try {
            
            const response = await fetch(`${backendURL}/api/app-users/id/${userId}`, {
                method: 'GET',
                credentials: 'include'  // To ensure cookies are included
            });
    
            if (response.ok) {
                const userInfo = await response.json();
                // 
                setUserData(userInfo);
                // setUserId(userInfo.user_id);
            }
        } catch (error) {
            console.error('Error fetching user info:', error);
            // Handle network errors
        }
    };

    const fetchUserType = async () => {
        
            try {
                const response = await fetch(`${backendURL}/api/usertypes/${userId}`,{
                    method: 'GET',
                    credentials: "include",
                })
                if (response.ok){
                    const data = await response.json();
                    setUserType(data);
                } else {
                }
                } catch (error){
                    console.error("Error fetching user type id: ",error)
                }
    };


    useEffect(() => {
        if (!userId) {
            const storedUserId = localStorage.getItem('userId');
            if (storedUserId) {
                setUserId(storedUserId);
            }
        }

        if (userId) {
            fetchUserInfo();
            fetchUserType();
        }
    }, [userId]);


    return (
        <AuthContext.Provider value={{ authState, fetchUserType, setAuthState, login, logout, checkAuth }}>
            <UserDataContext.Provider value={{ userData, setUserData, userType }}>
                {children}
            </UserDataContext.Provider>
        </AuthContext.Provider>
    );
};

export default AuthContext;
