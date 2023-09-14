import React,{ useEffect,useState } from "react";
import './SignUp.css';
import { useNavigate } from 'react-router-dom';
import AnimatedBackground from "./AnimatedBackground";
import axios from 'axios';
import { publicIp } from 'public-ip';
const SignUp = () => {
    const [isFlickering, setFlickering] = useState(true);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const navigate = useNavigate();

   
  useEffect(() => {
    const flickerInterval = setInterval(() => {
      setFlickering(Math.random() < 0.7); // 70% chance of flickering
    }, Math.random() * 500 + 200);

    const resetFlicker = () => {
      setFlickering(false);
      setTimeout(() => {
        setFlickering(Math.random() < 0.7); // 70% chance of flickering
        setTimeout(resetFlicker, Math.random() * 4000 + 1000); // Randomly wait before flickering back
      }, Math.random() * 4000 + 2000); // Randomly stay consistent for 2 to 6 seconds before flickering again
    };

    resetFlicker();

    return () => {
      clearInterval(flickerInterval);
    };
  }, []);
  const getIPAddress = async () => {
    let ipAddress;
    try {
      ipAddress = await publicIp();
    } catch (error) {
      console.error(`Error: ${error}`);
    }
    return ipAddress;
  }
  const handleSignUp = async () => {
    // Name validation
    if (!name.trim()) {
        alert("Name is required!");
        return;
    }

    if (/[^a-zA-Z\s]/.test(name)) {
        alert("Name should only contain letters and spaces.");
        return;
    }

    // Email validation
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailRegex.test(email)) {
        alert("Please enter a valid email address!");
        return;
    }

    if (email !== email.trim()) {
        alert("Email should not have leading or trailing spaces.");
        return;
    }

    // Password matching
    if (password !== repeatPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Password length
    if (password.length < 8) {
        alert("Password should be at least 8 characters long.");
        return;
    }

    if (password.length > 16) {
        alert("Password should not exceed 16 characters.");
        return;
    }

    if (password !== password.trim()) {
        alert("Password should not have leading or trailing spaces.");
        return;
    }

    // Password complexity
    if (!/[a-z]/.test(password) || !/[A-Z]/.test(password) || !/[0-9]/.test(password)) {
        alert("Password should contain at least one lowercase letter, one uppercase letter, and one number.");
        return;
    }

    const specialCharacters = /[ !@#`$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
    if (!specialCharacters.test(password)) {
        alert("Password should contain at least one special character.");
        return;
    }

    

    // If all validations pass, make the API call
    try {
        const ipAddress = await getIPAddress();
        const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/signup`, {
            name,
            email,
            password,
            ipAddress
        }, { withCredentials: true });

        if (response.data.message) {
            if (response.data.message.includes("Signup successful")) {
                alert("Signup successful! Please verify your email before logging in.");
                navigate('/login');
            } else {
                alert(response.data.message);
            }
        }
    } catch (error) {
        console.error('Error:', error);
        if (error.response && error.response.data && error.response.data.message) {
            alert(error.response.data.message);
        } else {
            alert("Signup failed. Please try again.");
        }
    }
};
    return (
        <div className="SignUp">
            <div className="animated-background-wrapper1">
            <AnimatedBackground/>
            </div>
            {isFlickering && <div className="catalyst_sign flicker">Catalyst</div>}
            {!isFlickering && <div className="catalyst_sign hidden">Catalyst</div>}
            <div className="signup-container">
                <h2>Sign Up</h2>
                <input type="text" placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
                <input type="email" placeholder="Email Address" value={email} onChange={e => setEmail(e.target.value)} />
                <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                <input type="password" placeholder="Repeat Password" value={repeatPassword} onChange={e => setRepeatPassword(e.target.value)} />
                <button className="signup-button" onClick={handleSignUp}>Sign Up</button>
                <p>Already a member? <a href="/login">Login now!</a></p>
            </div>
        </div>
    );
}

export default SignUp;