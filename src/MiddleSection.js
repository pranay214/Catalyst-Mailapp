import React, { useEffect,useState } from 'react';
import './MiddleSection.css';
import './button.css';
import  AnimatedBackground  from './AnimatedBackground';
import './Header.css';
import Demonstrate from './Demonstrate';

function MiddleSection() {
  const texts = [
    "Revolutionize your email outreach! Get on board the ultimate email sensation.",
    "Stay ahead of the competition with our cutting-edge email marketing solutions!",
    "Unlock the potential of personalized emails to engage and retain your audience.",
  ];

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFadeIn, setIsFadeIn] = useState(true);

  const switchText = () => {
    setIsFadeIn(false); // Fade out the current text
    setTimeout(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % texts.length); // Switch to the next text
      setIsFadeIn(true); // Fade in the next text
    }, 500); // 1 second for fade out animation
    setTimeout(() => {
      setIsFadeIn(false); // Fade out the next text after 4 seconds
    }, 4500); // 5 seconds total (including the 1 second for fade out)
  };

  useEffect(() => {
    const interval = setInterval(switchText, 5000); // 6 seconds (4 seconds for staying + 1 second for fade out + 1 second for fade in)
    return () => clearInterval(interval);
  }, []);


  const [isFlickering, setFlickering] = useState(true);

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
  
  return (
    <section className="middle-section">
      
        <div className="background-wrapper">
            <AnimatedBackground/>
        </div>

      {isFlickering && <div className="catalyst-text flicker">Catalyst</div>}
      {!isFlickering && <div className="catalyst-text hidden">Catalyst</div>}
    

    <div className="demon-holder">
      <Demonstrate/>
    </div>
    <div className="text-container">
    <p className={`fade-text ${isFadeIn ? 'fade-in' : ''}`}>
          {texts[currentIndex]}
        </p>
      <div className="button-container">
          <button className="button button-primary">Learn More</button>
          <button className="button button-secondary">Try it Now!</button>
        </div>
    </div>
   
  
  
  </section>
  );
}

export default MiddleSection;