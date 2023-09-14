import React,{ useCallback, useEffect,useState }  from "react";
import './Login.css';
import AnimatedBackground from "./AnimatedBackground";
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import jwt_decode from "jwt-decode";
import axios from 'axios';
import { publicIp } from 'public-ip';
import { useContext } from 'react';
import  UserContext  from './usercontext';



const Login = () => {
    const { setUser } = useContext(UserContext);
    const [isFlickering, setFlickering] = useState(true);
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

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
  const responseMessage = async (response) => {
    const token = response.credential;
    const decodedToken = jwt_decode(token);
    console.log(decodedToken);
    const profilePic = decodedToken.picture;
    const name = decodedToken.name;
    const email = decodedToken.email;
    const googleId = decodedToken.sub;
    const expiresIn = decodedToken.exp;
    const createdAt = decodedToken.iat;
  
    console.log(`Name: ${name}`);
    console.log(`Email: ${email}`);
    console.log(`Profile Picture: ${profilePic}`);
    
    try {
      const ipAddress = await getIPAddress();
      const res = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/login`, {
        token,
        profilePic,
        name,
        email,
        googleId,
        expiresIn,
        createdAt,
        ipAddress
      }, { withCredentials: true });
  
      if (res.data.message === 'Logged in.') {
        setUser({
          name,
          email,
          profilePic,
          googleId,
          expiresIn,
          createdAt
        });
          console.log(res.data); // log the data received from server
          navigate('/client');
        }   else {
          console.log('Failed to log in:', res.data.message);
        }
    } catch (error) {
      console.error(`Error: ${error}`);
      alert("Something went wrong. Try Again!");
    }
  };
  
  const errorMessage = (error) => {
    console.log(error);
  };


  const handleLocalLogin = async () => {
    if (!email || !password) {
        alert("Please fill in all fields.");
        return;
    }
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!email || !emailRegex.test(email)) {
        alert("Please enter a valid email address.");
        return;
    }
    if (!password) {
      alert("Please enter your password.");
      return;
    }

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/local-login`, {
            email,
            password
        }, { withCredentials: true });

        if (res.data.message === 'Logged in.') {
            setUser({
                name: res.data.name,
                email: res.data.email,
                profilePic: res.data.profilePic
            });
            navigate('/client');
        } else {
            alert(res.data.message);
        }
    } catch (error) {
        console.error(`Error: ${error}`);
        alert(error.response.data.message);
    }
};


    return (
        <div className="Login">
            <div className="animated-background-wrapper">
            <AnimatedBackground/>
            </div>
            {isFlickering && <div className="catalyst_new flicker">Catalyst</div>}
            {!isFlickering && <div className="catalyst_new hidden">Catalyst</div>}
        <div className="login-container">
            <h2>Login</h2>
            <input 
              type="email" 
              placeholder="Email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)}
          />
          <input 
              type="password" 
              placeholder="Password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)}
          />
            <button className="login-button" onClick={handleLocalLogin}>Login</button>
            <div className="google-login">
              <br />
              <br />
              <GoogleLogin onSuccess={responseMessage} onError={errorMessage} />
            </div>
            <p>Not a member yet? <Link to="/signup">Sign up now!</Link></p>
        </div>
        </div>
    );
}

export default Login;