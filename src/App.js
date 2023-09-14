import './App.css';
import Footer from './Footer';
import MiddleSection from './MiddleSection';
import AboutContent from './AboutContent';
import NewsLetter from './NewsLetter';
import Login from './Login';
import SignUp from './SignUp';
import { BrowserRouter as Router, Route, Routes,Link,Outlet,useLocation } from 'react-router-dom';
import { HashLink } from 'react-router-hash-link';
import Client from './Client'
import UserContext, { UserProvider } from './usercontext';
import UserMenu from './UserMenu';
import {useContext} from 'react';
import SettingsPage from './SettingsPage';
import PrivacyPolicy from './PrivacyPolicy';
import TermsnConditions from './TermsnConditions';
import Cookiepolicy from './Cookiepolicy';
import ProfileSettings from './ProfileSettings';

function App() {

  function Navigation() {
    const location = useLocation();
    const { user } = useContext(UserContext);
    
    return location.pathname === '/' ? (
      <header>
        {location.pathname === '/' && (
          <nav className={`nav-right ${user ? 'nav-shifted' : ''}`}>
            <ul>
              {!user && <li><Link className="nav-link" to="/">Home</Link></li>}
              {!user && <li><HashLink className="nav-link" to="/#about-content">About</HashLink></li>}
              {!user && <li><HashLink className="nav-link" to="/#footer">Contact</HashLink></li>}
              {!user && <li><Link className="nav-link" to="/login">Login</Link></li>}
            </ul>
          </nav>
        )}
        {user && <UserMenu />}
      </header>
    ) : null;
}

  return (
    <div className="App"> 
      <UserProvider> {/* added UserProvider */}
        <Router>
          <Navigation />
          <Routes>
            <Route path="/" element={
              <>
                <MiddleSection/>
                <AboutContent/>
                <NewsLetter/>
                <Footer />
              </>
            } />
            <Route path="/about" element={<AboutContent />} />
            <Route path="/login" element={<Login />} />
            <Route path="/client" element={<Client />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/settings" element={<SettingsPage/>} />
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />   
            <Route path="/terms-and-conditions" element={<TermsnConditions />} /> 
            <Route path="/cookie-policy" element={<Cookiepolicy/>} /> 
            {/* Add other routes as needed */}
          </Routes>
        </Router>
      </UserProvider> {/* closing UserProvider */}
    </div>
  );
}

export default App;