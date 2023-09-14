import React from 'react';
import './Cookiepolicy.css';
import Header from './Header';

function Cookiepolicy() {
    return (
        <div className="cookie-background">
        <Header/>
        <div className="cookie-card">
        <h1>Cookie Policy for Catalyst</h1>
        <p>Last updated: 11/08/2023</p>

        <h2>1. Introduction</h2>
        <p>Catalyst uses cookies to improve user experience, provide personalized content, and analyze our traffic. This policy provides information about the cookies we use and the purposes for which we use them.</p>
        <h2>2. What are cookies?</h2>
        <p>Cookies are small text files that are placed on your computer or mobile device when you visit a website. They are widely used to make websites work, or work more efficiently, as well as to provide information to the owners of the site.</p>
        <h2>3. How Catalyst uses cookies</h2>
        <p>Authentication: We use cookies to recognize you and remember your user preferences when logged into our app, ensuring you don't need to log in every time you visit.</p>
        <p>Security: Cookies help implement security features and detect malicious activities.</p>
        <p>Preferences: Cookies can tell us which language you prefer and what your communications preferences are.</p>
        <p>Analytics: We may use cookies to gather analytics about the usage and activity on our app.</p>
        <h2>4. Types of cookies we use</h2>
        <p>Session cookies: These are temporary cookies that are only accessible for the duration of a user's session. They are deleted when a user closes the web browser.</p>
        <p>Persistent cookies: These cookies remain on a user's device even after closing the web browser. They are used to remember user preferences and actions within the website.</p>
        <h2>5. Third-party cookies</h2>
        <p>We may use third-party services or plugins that set their own cookies. These cookies are governed by the respective third-party's policies.</p>
        <h2>6. Managing cookies</h2>
        <p>Most web browsers allow you to control cookies through their settings. You can:</p>
        <p>Delete all cookies: This will remove all cookies and you will lose any saved preferences on websites you visit.</p>
        <p>Block cookies: You can set your browser to block all or some cookies. Note that if you block all cookies, many websites (including ours) may not work properly.</p>
        <p>Manage cookies: You can set exceptions for some websites or domains in your browser settings.</p>
        <h2>7. Changes to this Cookie Policy</h2>
        <p>We may update our Cookie Policy from time to time. We will notify you of any changes by posting the new Cookie Policy on this page.</p>
        <h2>8. Contact Us</h2>
        <p>If you have any questions about this Cookie Policy, please contact us at admin@catalyst-tech.in.</p>
        </div>
        </div>
         );
        }
        
        export default Cookiepolicy;