import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ProfileSettings.css';
import { FaUpload } from 'react-icons/fa'; // Importing the upload icon

function ProfileSettings() {
    const [user, setUser] = useState({});
    const [selectedFile, setSelectedFile] = useState(null);
    
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/check_auth`, { withCredentials: true });
                if (res.status === 200) {
                    setUser(res.data.user);
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        };

        fetchUserData();
    }, []);

    const handleImageChange = (e) => {
        setSelectedFile(e.target.files[0]);
        // You can add code here to upload the image to your server if needed
    };

    return (
        <div className="card-containerp">
            <div className="main-contentp">
                <h2>Profile Settings</h2>
                <div className="separator1"></div>
                <div className="profile-image-container">
                    <img src={user.profilePic || "path_to_default_image.jpg"} alt="Profile" className="profile-image" />
                    <label className="image-upload-label">
                        <FaUpload className="upload-icon" />
                        <input type="file" onChange={handleImageChange} className="image-upload" />
                    </label>
                </div>
                <p>Email: {user.email}</p>
                {/* Add more elements here as needed */}
            </div>
        </div>
    );
}

export default ProfileSettings;