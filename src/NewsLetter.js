import React from 'react';
import './NewsLetter.css';
import './button.css';


function NewsLetter() {
    return (
    <section className="news_letter">
        
        <div class="form-container">
            <h1>Subscribe to exclusive development updates!</h1>
            <form id="subscribe-form" action="https://submit-form.com/wliMXczM">
                <div class="form-row">
                    <input type="text" id="name" name="name" placeholder="Name" required/>
                    <input type="email" id="email" name="email" placeholder="Email Address" required/>
            </div>

            <div class="form-row">
                <textarea id="message" name="message" rows="4" placeholder="Message" required></textarea>
            </div>
                <button type="submit">Submit</button>
            </form>
        </div>
    </section>
    );
  }
  
  export default NewsLetter;