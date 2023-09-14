import React from 'react';
import './Footer.css';

function Footer() {
  return (
    <section id="footer">
      <footer className="footer">
        <div className="footer-content">
        <span className="footer-brand">@Catalyst 2023 Pvt. Ltd.</span>
          <div className="footer-links">
            <a href="/privacy-policy">Privacy Policy</a> | 
            <a href="/terms-and-conditions">Terms & Conditions</a> | 
            <a href="/cookie-policy">Cookie Policy</a>
          </div>
        </div>
      </footer>
    </section>
  );
}

export default Footer;