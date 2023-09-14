import React, { useEffect, useState } from 'react';
import './fadeAnimation.css'; // Import the fadeAnimation.css

const AnimatedText = ({ texts, currentIndex }) => {
  return <p className="fade-text">{texts[currentIndex]}</p>;
};

export default AnimatedText;