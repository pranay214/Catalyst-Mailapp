import React, { useEffect,useState } from 'react';
import './Demonstrate.css';
import Macbook from './mac.png'
import em from './1.png'
import em2 from './4.png'

function Demonstrate() {
    return (
      <div className="Demonstrate">
        <div className="macbook-container">
          <img src={Macbook}/> 
        <div className="Message-contain">    
        <img src={em}/>
        <img src={em2}/>
        </div>
      </div>
      </div>

    );
}
export default Demonstrate;
