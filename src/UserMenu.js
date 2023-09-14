import React, { useState, useContext, useRef, useEffect } from 'react';
import UserContext from './usercontext';
import { Link,useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './UserMenu.css'
import { FaUserCircle, FaSignOutAlt, FaHome } from 'react-icons/fa';

function UserMenu() {
    const [open, setOpen] = useState(false);
    const { user, setUser } = useContext(UserContext);
    const location = useLocation(); 
    const navigate = useNavigate();
    const menuRef = useRef(null);

    const { profilePic } = user || {};

    const toggleOpen = () => setOpen(!open);

    const logout = async () => {
        try {
            await axios.post(`${process.env.REACT_APP_API_BASE_URL}/logout`, {}, { withCredentials: true });
            setUser(null);
            navigate('/');
        } catch (err) {
            console.error('Logout failed', err);
        }
    };

    useEffect(() => {
        const handleClickOutsideMenu = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setOpen(false);
            }
        }
        // Add the event listener when the component mounts
        document.addEventListener('mousedown', handleClickOutsideMenu);
        // Clean up the event listener on component unmount
        return () => {
            document.removeEventListener('mousedown', handleClickOutsideMenu);
        }
    }, []);

    if (!user) {
        return null;
    }

    return (
        <div className="user-menu" ref={menuRef}>
            <img
                src={profilePic || "https://via.placeholder.com/150"} // Fallback URL in case `profilePic` is null or undefined
                alt="User"
                onClick={toggleOpen}
                className="user-avatar"
            />
            {open && (
                <div className="user-dropdown">
                    <Link to="/settings" className="user-dropdown-item"><FaUserCircle color="#ff6347" /> Settings</Link>
                    {location.pathname === '/' && <Link to="/client" className="user-dropdown-item"><FaHome color="#32cd32" /> Dashboard</Link>}
                    <span onClick={logout} className="user-dropdown-item"><FaSignOutAlt color="#f0e130" /> Logout</span>
                </div>
            )}
        </div>
    );
}

export default UserMenu;