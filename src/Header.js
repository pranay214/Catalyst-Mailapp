import React, { useEffect, useState } from 'react';
import './Header.css';
import  AnimatedBackground  from './AnimatedBackground';

  
function Header() {
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
    <header className="header">
      <div className="Header-wrap">
        
        </div>
        {isFlickering && <div className="catalyst-text flicker">Catalyst</div>}
      {!isFlickering && <div className="catalyst-text hidden">Catalyst</div>}
    </header>
  );
}

export default Header;