import React, { useRef } from 'react';
import { Link,useNavigate } from 'react-router-dom';
import UserContext from './usercontext';
import './SettingsPage.css';
import UserMenu from './UserMenu';
import Header from './Header';
import axios from 'axios';
import { useState,useEffect } from 'react';
import { FaInfo, FaKey,FaUser} from 'react-icons/fa';
import ProfileSettings from './ProfileSettings';





function SettingsPage() {
    const navigate = useNavigate();
    const [sessionExpired, setSessionExpired] = useState(false);
    const { user } = React.useContext(UserContext);
    const [apiKey, setApiKey] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [emailProvider, setEmailProvider] = useState('');
    const [isNavVisible, setIsNavVisible] = useState(false);
    const [showProfileSettings, setShowProfileSettings] = useState(false);
    const navPanelRef = useRef(null); // Create a reference for the nav panel
   
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (navPanelRef.current && !navPanelRef.current.contains(event.target)) {
                setIsNavVisible(false); // Hide the nav panel if click was outside
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            // Cleanup the event listener on component unmount
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);


    useEffect(() => {
        const checkSession = async () => {
            try {
                const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/check_auth`, { withCredentials: true });
    
                if (res.status !== 200) {
                    setSessionExpired(true);
                    navigate('/login');
                }
            } catch (error) {
                console.error('An error occurred:', error);
                setSessionExpired(true);
                navigate('/login');
            }
        };
    
        checkSession();
    }, []);

    if (!user) {
        return null;
    }

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        
        // Add a check for emailProvider
        if (!email || !password || !emailProvider) {
            alert("All fields are required!");
            return;
        }
    
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailRegex.test(email)) {
            alert("Please enter a valid email address!");
            return;
        }
    
        // Include emailProvider in the data object
        const data = {
            apiKey: apiKey,
            email: email,
            password: password,
            emailProvider: emailProvider
        };
    
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/credentials`, data, { withCredentials: true });
            console.log(response.data);
            alert("Data saved successfully!")
        } catch (error) {
            console.error('Error:', error);
            
            if (error.response && error.response.data && error.response.data.message) {
                alert(error.response.data.message);
            } else {
                alert("Something went wrong. Try again!");
            }
        }
    }


    

    
    
    const toggleProfileSettings = () => {
        setShowProfileSettings(!showProfileSettings);
    }

    return (
        <div className="settings-page">
            <div className="orig-header">
               <Header/>
                {/* Nav Toggle Button for Mobile */}
                <button className="nav-toggles" onClick={() => setIsNavVisible(!isNavVisible)}>☰</button> 
            </div>
            
            <div className="settings-header">
            <UserMenu/>
            </div>  
            <div class="content-wrappers">

            <div className="settings-content">
            <div className={`nav-panels ${isNavVisible ? 'show' : ''}`} ref={navPanelRef}>
                        <button onClick={toggleProfileSettings}>
                            <FaKey color="#FFA726" /> Credentials
                        </button>
                        <button onClick={toggleProfileSettings}>
                            <FaUser color="#4CAF50" /> Profile
                        </button>
                    </div>
                    {showProfileSettings ? (
                        <ProfileSettings />
                    ) : (
                <form className="client-form" onSubmit={handleFormSubmit}>
                    <h2>Save Credentials</h2>
                    <div className="separator"></div>
                    <label>
                        OpenAI API Key
                        <div className="info-icon-container">
                            <FaInfo className="info-icon" />
                            <div className="tooltip">We current do not support user API support. You can leave this input blank.</div>
                        </div>
                        <input type="text" placeholder="OpenAI API Key" value={apiKey} onChange={e => setApiKey(e.target.value)} />
                    </label>
                    <label>
                        Email Provider
                        <div className="info-icon-container2">
                            <FaInfo className="info-icon" />
                            <div className="tooltip">We support the following providers.You can request your preferred service by mailing us. </div>
                        </div>
                        <select className="custom-select" value={emailProvider} onChange={e => setEmailProvider(e.target.value)}>
                        <option value="gmail">Gmail</option>
                        <option value="yahoo">Yahoo</option>
                        <option value="outlook">Outlook</option>
                        <option value="godaddy">GoDaddy</option> 
                    </select>
                    </label>
                    <label>
                        Email ID
                        <input type="email" placeholder="Email ID" value={email} onChange={e => setEmail(e.target.value)} />
                    </label>
                    <label>
                        Email Password
                        <div className="info-icon-container3">
                            <FaInfo className="info-icon" />
                            <div className="tooltip">
                                If your mail is protected by 2-factor authentication, you may need an app-specific password. 
                                <a href="https://support.google.com/accounts/answer/185833?hl=en#zippy=" target="_blank" rel="noopener noreferrer">Read more</a>
                            </div>
                        </div>
                        <input type="password" placeholder="Email Password" value={password} onChange={e => setPassword(e.target.value)} />
                    </label>
                    <div className="new-b">
                        <button type="submit">SAVE</button>
                    </div>
                </form>
                 )}
            </div>  
            </div>     
        </div>
    );
}


export default SettingsPage;