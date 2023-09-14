import React from 'react';
import './PrivacyPolicy.css';
import Header from './Header';

function PrivacyPolicy() {
    return (
      <div className="privacy-policy-background">
        <Header/>
        <div className="privacy-policy-card">
          <h1>Privacy Policy for Catalyst</h1>
          <p>Last updated: 11/08/2023</p>
  
          <h2>1. Introduction</h2>
          <p>Welcome to Catalyst. We respect your privacy and are committed to protecting your personal data. This privacy policy will inform you about how we handle your personal data, your privacy rights, and how the law protects you.</p>

          <h2>2. Data We Collect</h2>
          <p>Based on our previous conversations, we collect the following data:</p>
          <h3>User Information:</h3>
          <p>This includes your name, email address, profile picture, and Google ID.</p>
          <h3>Session Information: </h3>
          <p>We use cookies to manage user sessions. This includes session IDs.</p>
          <h3>IP Address:</h3>
          <p>We log IP addresses for security purposes and to ensure the best user experience.</p>
          <h2>How We Use Your Data</h2>
          <p>Authentication: To log you into our app and ensure only authorized users access certain parts of the app.</p>
          <p>Security: To protect our app from malicious attacks and to ensure the safety of our users' data.</p>
          <p>User Experience: To provide a personalized experience for our users.</p>

          <h2>4. Cookies</h2>
          <p>We use cookies to manage user sessions. Cookies are small files placed on your device that allows our app to recognize you and remember your preferences.</p>
          <h2>5. Data Sharing</h2>
          <p>We do not sell or share your personal data with third parties for their marketing purposes. We might share data with third-party service providers who assist us in operating our app, conducting our business, or serving our users, as long as those parties agree to keep this information confidential or may be required by the local law of the land.</p>
          <h2>6. Data Security</h2>
          <p>We implement a variety of security measures to maintain the safety of your personal information. Your personal information is stored behind secured networks and is only accessible by a limited number of persons who have special access rights to such systems and are required to keep the information confidential. Though we take all necessary steps to protect your data, unseen circumstances can always result in data loss, and we take no liability in such a case of data loss.</p>

          <h2>7. Your Rights</h2>
          <p>You have the right to access, update, or delete your personal data. If you wish to exercise these rights, please contact us.</p>

          <h2>8. Changes to This Privacy Policy</h2>
          <p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page.</p>
          <h2>Contact Us</h2>
          <p>If you have any questions about this Privacy Policy, please contact us at admin@catalyst-tech.in.</p>
        </div>
      </div>
    );
  }
  
  export default PrivacyPolicy;