import React from 'react';
import { useInView } from 'react-intersection-observer';
import { useSpring, animated,config } from 'react-spring';
import './AboutContent.css';
import email from './Bounce.jpg';
import personalize from './Emails.jpg';


const AboutContent = () => {
  const [ref1, inView1] = useInView({ triggerOnce: true });
  const [ref2, inView2] = useInView({ triggerOnce: true });

  const animation1 = useSpring({
    config: { ...config.default, friction: 100 },
    opacity: inView1 ? 1 : 0,
    transform: inView1 ? 'translate3d(0,0,0)' : 'translate3d(0,50px,0)',
  });

  const animation2 = useSpring({
    config: { ...config.default, friction: 100 },
    opacity: inView2 ? 1 : 0,
    transform: inView2 ? 'translate3d(0,0,0)' : 'translate3d(0,50px,0)',
  });

  return  (
    <section id="about-content">
    <div className="about-content">
      <div className="container">
        <animated.div className="left_container" ref={ref1} style={animation1}>
          <h1>Struggling with bouncing emails? We’ve got your back!</h1>
          <p>Our state-of-the-art email validation system is designed to take the guesswork out of your outreach game. Get ready to experience unparalleled delivery rates, enhanced engagement, and boosted ROI.</p>
        </animated.div>
        <animated.div className="right_container" ref={ref1} style={animation1}>
        <img className='img1' src={email} alt="Email Icon" />
        </animated.div>
      </div>
      <div className="container">
        <animated.div className="left_container" ref={ref2} style={animation2}>
          <img className='img2' src={personalize} alt="Email Icon" />
        </animated.div>
        <animated.div className="right_container" ref={ref2} style={animation2}>
          <h1>Don’t just automate – Personalize like a pro!</h1>
          <p>Our AI-driven email personalization engine uses advanced algorithms and data analysis techniques to ensure that your emails are carefully personalized for different leads.</p>
        </animated.div>
      </div>
    </div>
    </section>
  );
};

export default AboutContent;