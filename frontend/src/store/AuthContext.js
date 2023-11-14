import React, { createContext, useState, useContext, useEffect } from 'react';
import { backendURL } from '../IPaddress';

const AuthContext = createContext();
const UserDataContext = createContext();

export const useAuth = () => useContext(AuthContext);
export const useUserData = () => useContext(UserDataContext);

export const AuthProvider = ({ children, navigate }) => {
    const [authState, setAuthState] = useState(false);
    const [userData, setUserData] = useState(null);
    const [userId, setUserId ] = useState('');


    const login = async (user, password) => {
        const response = await fetch(`${backendURL}/api/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${user}&password=${encodeURIComponent(password)}`,
            credentials: 'include',
        });
        if (response.ok) {
            setAuthState(true);           
            // Fetch user info right after setting the username
            await fetchUserInfo();
            navigate('/main');
        }
    };

    const logout = async () => {
        await fetch(`${backendURL}/api/logout/`, {
            method: 'POST',
            credentials: 'include',
        });
        setAuthState(false);
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
                const data = await response.json(); // Wait for the promise to resolve
                // Use 'data' as needed
                setUserId(data);
                setAuthState(true);
                try{
                    await fetchUserInfo(data);
                } catch (error) {
                    console.error("Error fetching the user info", error)
                }
                
            } catch (error) {
                console.error("Error reading response data:", error);
                // Handle any errors that occur during JSON parsing
            }
        } else {
            console.log("Failed response: ", response);
            setAuthState(false);
            // navigate('/login');
            
        }
    };

    const fetchUserInfo = async (userId) => {
        console.log("username parameter: ", userId);
        try {
            const response = await fetch(`${backendURL}/api/app-users/id/${userId}`, {
                method: 'GET',
                credentials: 'include'  // To ensure cookies are included
            });
    
            if (response.ok) {
                const userInfo = await response.json();
                console.log("Success! Userinfo: ", userInfo);
                setUserData(userInfo);
                setUserId(userInfo.user_id);
            }
        } catch (error) {
            console.error('Error fetching user info:', error);
            // Handle network errors
        }
    };

    useEffect(() => {
        if (authState) {
            checkAuth();
            fetchUserInfo();
        }
    }, [authState]);


    return (
        <AuthContext.Provider value={{ authState, setAuthState, login, logout, checkAuth }}>
            <UserDataContext.Provider value={{ userData, setUserData }}>
                {children}
            </UserDataContext.Provider>
        </AuthContext.Provider>
    );
};

export default AuthContext;
