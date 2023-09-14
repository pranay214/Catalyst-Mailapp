import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import Select from 'react-select';
import 'react-datepicker/dist/react-datepicker.css';
import './PanelFive.css'
import axios from 'axios';

const PanelFive = () => {
    const [startDate, setStartDate] = useState(new Date());
    const [leadsFile, setLeadsFile] = useState(null);

    const TimeComponent = ({ onChange, value }) => {
        const times = [];
        for (let i = 0; i < 24; i++) {
            for (let j = 0; j < 60; j += 15) {
                times.push({
                    value: `${i.toString().padStart(2, '0')}:${j.toString().padStart(2, '0')}`,
                    label: `${i.toString().padStart(2, '0')}:${j.toString().padStart(2, '0')}`
                });
            }
        }

        return (
            <Select
                options={times}
                isSearchable={false}
                onChange={option => {
                    const [hours, minutes] = option.value.split(':');
                    const newDate = new Date(value);
                    newDate.setHours(hours);
                    newDate.setMinutes(minutes);
                    onChange(newDate);
                }}
                value={{ value, label: value.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }) }}
            />
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const now = new Date();
        if (startDate <= now) {
            alert('Invalid date. Please select a future date and time.');
            return;  // Exit the function early
        }

        const formData = new FormData();
        formData.append('scheduled_date', startDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }));
        formData.append('scheduled_time', startDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }));
        formData.append('leads', leadsFile);
    
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/schedule_email`, formData, { withCredentials: true });
            alert("Your emails have been scheduled!");
        } catch (error) {
            console.error('Error occurred:', error);
        
            // Check the specific error messages and alert accordingly
            if (error.response) {
                switch (error.response.data.message) {
                    case 'User data not saved. Please save user details first.':
                        alert('User data not found. Please save details in email wizard.');
                        break;
                    case 'Session ID missing.':
                        alert('Session ID is missing. Please log in again.');
                        break;
                    case 'Invalid session_id.':
                        alert('Invalid session. Please log in again.');
                        break;
                    case 'Scheduled date and time are required.':
                        alert('Please provide both the scheduled date and time.');
                        break;
                    case 'Invalid date. Please select a future date and time.':
                        alert('Invalid date. Please select a future date and time.');
                        break;
                    case 'Invalid date or time format.':
                        alert('Invalid date or time format. Please check and try again.');
                        break;
                    case 'Leads file is required.':
                        alert('Please upload the leads file.');
                        break;
                    case 'Invalid leads file format. Missing columns.':
                        alert('Invalid leads file format. Ensure the file has the required columns.');
                        break;
                    default:
                        alert('An error occurred. Please try again.');
                }
            } else {
                alert('An unexpected error occurred. Please try again.');
            }
        }
                    
    };

    return (
        <div className="card-container">
            <div className="main-content5">
                <form className="schedule-form" onSubmit={handleSubmit}>
                    <h2>Schedule for new Leads</h2>
                    <div className="separator"></div>
                    <div className="date-picker-container">
                        <label>Select Date:</label>
                        <DatePicker
                            selected={startDate}
                            onChange={date => setStartDate(date)}
                            dateFormat="MMMM d, yyyy"
                        />
                        <label>Select Time:</label>
                        <TimeComponent value={startDate} onChange={setStartDate} />
                    </div>
                    <div className="file-input-container">
                        <label>Select or Upload Leads:</label>
                        <input type="file" name="leads" onChange={(e) => setLeadsFile(e.target.files[0])} />
                    </div>
                    <button type="submit" className="schedule-button">SCHEDULE</button>
                </form>
            </div>
        </div>
    );
};

export default PanelFive;