import React, { useState,useContext,useEffect,useRef } from 'react';
import './Client.css'
import Header from './Header';
import axios from 'axios'; 
import { useNavigate } from 'react-router-dom';
import  UserContext  from './usercontext';
import UserMenu from './UserMenu';
import Countdown from 'react-countdown';
import './Header.css';
import PanelFive from './PanelFive';
import { FaMailBulk, FaDigitalTachograph, FaChartBar, FaEnvelope, FaCalendarAlt } from 'react-icons/fa';

const PanelOne = ({ showTemplateModal,handleTemplateSelect,prevTemplate,nextTemplate,setShowTemplateModal,formData,selectedTemplateIndex,templates,currentTemplateIndex, handleInputChange, handleFileUpload, handleFormSubmit,handleSaveDetails,handleSendMail,handleFinalSend}) => (
    <div className="panelone">
              {showTemplateModal && (
    <div className="modal">
        <div className="modal-content">
            <h2>Select a Template</h2>
            <div dangerouslySetInnerHTML={{ __html: templates[currentTemplateIndex] }}></div>
            <button onClick={() => handleTemplateSelect(currentTemplateIndex)}>Select</button>
            <button onClick={prevTemplate}>Previous</button>
            <button onClick={nextTemplate}>Next</button>
            <button onClick={() => setShowTemplateModal(false)}>Cancel</button>
        </div>
    </div>
)}
        <div className="main-content1">
            <form className="client-form">
                <label>
                    <span>Your company's USP</span>
                    <input 
                        type="text"
                        name="USP"
                        placeholder="USP"
                        value={formData.USP}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Your Offer, eg. Buy 1 get 1 free</span>
                    <input 
                        type="text"
                        name="offer"
                        placeholder="offer"
                        value={formData.offer}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Your Company's Name</span>
                    <input 
                        type="text"
                        name="Company_Name"
                        placeholder="Company Name"
                        value={formData.Company_Name}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Your Name</span>
                    <input 
                        type="text"
                        name="Owner_Name"
                        placeholder="Owner Name"
                        value={formData.Owner_Name}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Phone Number</span>
                    <input 
                        type="text"
                        name="Phone_number"
                        placeholder="Phone number"
                        value={formData.Phone_number}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Company Website</span>
                    <input 
                        type="text"
                        name="Website"
                        placeholder="Website"
                        value={formData.Website}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Consultation Link</span>
                    <input 
                        type="text"
                        name="Consultation_link"
                        placeholder="Consultation link"
                        value={formData.Consultation_link}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Your Service, eg. SMMA, AAA etc.</span>
                    <input 
                        type="text"
                        name="Service"
                        placeholder="Service"
                        value={formData.Service}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Your Customer type</span>
                    <input 
                        type="text"
                        name="Customer"
                        placeholder="Customer type"
                        value={formData.Customer}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    <span>Your broad industry, eg. Marketing, Automation etc.</span>
                    <input 
                        type="text"
                        name="Industry"
                        placeholder="Industry"
                        value={formData.Industry}
                        onChange={handleInputChange}
                    />
                </label>
                {/* Repeat for other input fields */}
                
                <input type="file" onChange={handleFileUpload} />
                
                {/* Button Group */}
                <div className="button-group">
                    <button type="submit" onClick={handleFormSubmit}>Generate</button>
                    <button className="save-button" type="button" onClick={handleSaveDetails}>Save details</button>
                    <button className="send-button" type="button" onClick={handleSendMail}>Send</button>
                </div>
            </form>
        </div>
        </div>
);

const PanelTwo = () => (
    <div className="paneltwo">
        <h2>Coming Soon!</h2>
    </div>
);

const PanelThree = () => (
    <div className='panelthree'>
        <h2>Coming Soon!</h2>
    </div>
);

const PanelFour = ({ templates,nextTemplate,prevTemplate,currentTemplateIndex }) => {
    const [emails, setEmails] = useState([]);
    const [selectedEmailIndex, setSelectedEmailIndex] = useState(null);
    const isMobile = window.innerWidth <= 600;
    const [showCheckboxes, setShowCheckboxes] = useState(true);
    const [pressTimer, setPressTimer] = useState(null); // Timer for long press
    const [selectedEmails, setSelectedEmails] = useState({});
    const selectAllCheckboxRef = useRef(null);
    const [showTemplateModal, setShowTemplateModal] = useState(false);
    const [selectedTemplateIndex, setSelectedTemplateIndex] = useState(null);

    useEffect(() => {
      axios
        .get(`${process.env.REACT_APP_API_BASE_URL}/emails`, { withCredentials: true })
        .then((res) => setEmails(res.data))
        .catch((err) => alert(err));
    }, []);

    const allChecked = emails.length > 0 && Object.keys(selectedEmails).length === emails.length && Object.values(selectedEmails).every(val => val);

    const handleRowClick = (index, e) => {
        if (e.target.type !== "checkbox") {
            setSelectedEmailIndex(index);
        }
    };
    const handleTemplateModalOpen = () => {
        setShowTemplateModal(true);
    };

    const handleTemplateSelect = (templateIndex) => {
        setSelectedTemplateIndex(templateIndex);
        setShowTemplateModal(false);
        handleFinalSend(templateIndex); // Send the email after selecting the template
    };

    const handleFinalSend = (templateIndex) => {
        const selectedTemplateContent = templates[templateIndex];
        const selectedEmailIds = Object.keys(selectedEmails).filter(emailId => selectedEmails[emailId]);

        // Make a POST request to the send_selected_emails endpoint
        axios.post(`${process.env.REACT_APP_API_BASE_URL}/send_selected_emails`, { 
            template: selectedTemplateContent,
            emailIds: selectedEmailIds
        }, { withCredentials: true })
        .then(response => {
            console.log(selectedEmailIds);
            console.log(response.data);
            alert("Mails sent successfully!");
        })
        .catch(error => {
            // Handle the error as needed
            console.error(error);
            alert(error.response.data.message);
        });
    };

    const handleSelectAll = () => {
        if (allChecked) {
            setSelectedEmails({});
        } else {
            const allEmailsSelected = emails.reduce((acc, email) => {
                acc[email.id] = true;
                return acc;
            }, {});
            setSelectedEmails(allEmailsSelected);
        }
    };
    const handleSelectAllCheckboxClick = () => {
        if (allChecked) {
            setSelectedEmails({});
        } else {
            const allEmailsSelected = emails.reduce((acc, email) => {
                acc[email.id] = true;
                return acc;
            }, {});
            setSelectedEmails(allEmailsSelected);
        }
    };

    const handleTouchStart = (e) => {
        if (e.target.type !== "checkbox") {
            setPressTimer(setTimeout(() => {
                setShowCheckboxes(true);
                if (selectAllCheckboxRef.current) {
                    selectAllCheckboxRef.current.classList.add('show-checkbox');
                }
            }, 500));
        }
    };
    
    const handleTouchEnd = () => {
        clearTimeout(pressTimer);
    };

    const closePopup = () => {
      setSelectedEmailIndex(null);
    };

    const handleCheckboxClick = (emailId, e) => {
        e.stopPropagation(); // Prevents the event from bubbling up
        setSelectedEmails(prev => ({ ...prev, [emailId]: !prev[emailId] }));
    };
    const handleIndividualCheckboxClick = (emailId) => {
        setSelectedEmails(prev => ({ ...prev, [emailId]: !prev[emailId] }));
    };

   
    return (
        <div className="panelfour">
            <button className="send-selected-btn" onClick={handleTemplateModalOpen}>SEND</button>
            
            {showTemplateModal && (
                <div className="modal">
                    <div className="modal-content">
                        <h2>Select a Template</h2>
                        <div dangerouslySetInnerHTML={{ __html: templates[currentTemplateIndex] }}></div>
                        <button onClick={() => handleTemplateSelect(currentTemplateIndex)}>Select</button>
                        <button onClick={prevTemplate}>Previous</button>
                        <button onClick={nextTemplate}>Next</button>
                        <button onClick={() => setShowTemplateModal(false)}>Cancel</button>
                    </div>
                </div>
            )}
            <div className="email-card">
            <div className="email-header">
            <div className="select-all-container">
                <input 
                    ref={selectAllCheckboxRef}
                    type="checkbox" 
                    className="select-all-checkbox" 
                    checked={allChecked} 
                    onChange={handleSelectAllCheckboxClick}
                />
                <span>All</span>
            </div>
                <div>ID</div>
                <div>Email Content</div>
                <div>Generated At</div>
                <div>Sent At</div>
                <div>Targeted Company</div>
                </div>
                {emails.map((email, index) => (
                <div
                    key={email.id}
                    className={`email-row ${showCheckboxes ? 'show-checkbox' : ''}`}
                    onClick={(e) => handleRowClick(index, e)}
                    onTouchStart={handleTouchStart}
                    onTouchEnd={handleTouchEnd}
                >
                    {showCheckboxes && 
                         <input 
                         type="checkbox" 
                         className="email-checkbox" 
                         checked={selectedEmails[email.id] || false}
                         onChange={(e) => {
                             e.stopPropagation();
                             handleIndividualCheckboxClick(email.id);
                         }}
                     />
                    }
                        <div>{index + 1}</div>
                        <div>
                          {email.email_content && typeof email.email_content === "string"
                            ? email.email_content.split("\n")[0]
                            : "No content"}
                        </div>
                        <div>
                          {new Date(email.generated_at).toLocaleString(undefined, {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </div>
                        <div>
                          {email.sent_at
                            ? new Date(email.sent_at).toLocaleString(undefined, {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })
                            : "Not sent"}
                        </div>
                        <div>{email.targeted_company}</div>
                    </div>
                ))}
            </div>
            {selectedEmailIndex !== null && (
              <div className="email-popup-overlay" onClick={closePopup}>
                <div className="email-popup">
                  <p>{emails[selectedEmailIndex].email_content}</p>
                </div>
              </div>
            )}
        </div>
    );
};


function Client() {
    const { user } = useContext(UserContext);
    const navigate = useNavigate();
    const [showTemplateModal, setShowTemplateModal] = useState(false);
    const [selectedTemplateIndex, setSelectedTemplateIndex] = useState(null);
    const [templates, setTemplates] = useState([]);
    const [sessionExpired, setSessionExpired] = useState(false);
    const [currentTemplateIndex, setCurrentTemplateIndex] = useState(0);

    useEffect(() => {
        const panelOne = document.querySelector('.client');
        const navPanel = document.querySelector('.nav-panel');
    
        if (panelOne && navPanel) {
            navPanel.style.height = `${panelOne.offsetHeight}px`;
        }
    }, [])
    
    const [formData, setFormData] = useState({
        USP: '',
        offer: '',
        Company_Name: '',
        Owner_Name: '',
        Phone_number: '',
        Website: '',
        Consultation_link: '',
        Service: '',
        Customer: '',
        Industry: '',
        // Add other fields as required
    });
    useEffect(() => {
        // Fetch templates from the backend when the component mounts
        axios.get(`${process.env.REACT_APP_API_BASE_URL}/get_templates`) // replace with your endpoint
            .then(response => {
                setTemplates(response.data.templates);
            })
            .catch(error => {
                console.error("Error fetching templates:", error);
            });
    }, []);
    const handleTemplateModalOpen = () => {
        setShowTemplateModal(true);
    };
    const handleTemplateSelect = (templateIndex) => {
        setSelectedTemplateIndex(templateIndex);
        setShowTemplateModal(false);
        handleFinalSend(templateIndex); // Send the email after selecting the template
    };

    const handleFinalSend = (templateIndex) => {
        const selectedTemplateContent = templates[templateIndex];
        // Make a POST request to the send_mail endpoint
        axios.post(`${process.env.REACT_APP_API_BASE_URL}/send_email1`, { template: selectedTemplateContent }, { withCredentials: true })
            .then(response => {
                // Handle the response as needed
                console.log(response.data);
                alert("Mails sent sucessfully!");
            })
            .catch(error => {
                // Handle the error as needed
                console.error(error);
                alert(error.response.data.message);
            });
    };

    const handleInputChange = (event) => {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    };

    // Add a state for the uploaded file
    const [uploadedFile, setUploadedFile] = useState(null);

    // Handle the file upload
    const handleFileUpload = (event) => {
        setUploadedFile(event.target.files[0]);
    };

    const [panel, setPanel] = useState('one');
    const [mails, setMails] = useState([]);
    const [showPopup, setShowPopup] = useState(false);
    const [spinnerMessage, setSpinnerMessage] = useState("Processing leads. Please wait!");
    const [remainingTime, setRemainingTime] = useState(null);
    const [processedLeads, setProcessedLeads] = useState(0);
    const [showSpinner, setShowSpinner] = useState(false);
    const [formSubmitted, setFormSubmitted] = useState(false);
   
    
    useEffect(() => {
        if (remainingTime > 0) {
          const timer = setInterval(() => {
            setRemainingTime((time) => (time - 1).toFixed(2));
          }, 1000);
          return () => clearInterval(timer);
        }
      }, [remainingTime]);

    const handleFormSubmit = async (event) => {
        event.preventDefault();
    
        
        if (!formData.USP || !formData.offer || !formData.Company_Name || !formData.Owner_Name || 
            !formData.Service || !formData.Customer || !formData.Industry) {
            alert('Please fill out all the fields.');
            return;
        }

        if (!/^\d{10}$/.test(formData.Phone_number)) {
            alert('Please enter a valid 10-digit phone number.');
            return;
        }

        const urlPattern = new RegExp('^(https?:\\/\\/)?' + // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
        '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
        if (!urlPattern.test(formData.Website) || !urlPattern.test(formData.Consultation_link)) {
            alert('Please enter a valid URL for the website and consultation link.');
            return;
        }


        if (!uploadedFile) {
            alert('Please upload a leads file.');
            return;
        }
    
        // Check file type (assuming you expect a CSV file)
        if (!uploadedFile.name.endsWith('.csv')) {
            alert('Invalid file type. Please upload a CSV file.');
            return;
        }

        if (mailsGenerated >= maxMails) {
            alert("Your mail subscription limit has been exhausted!");
            return; // Stop further processing.
        }

        let data = new FormData();
        Object.keys(formData).forEach(key => {
            data.append(key, formData[key]);
        });
        if (uploadedFile) {
            data.append('Leads', uploadedFile);
        }
        setSpinnerMessage("Processing leads");
        setShowSpinner(true);
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/process_leads`, data, { 
                withCredentials: true
            });
            if (response.data.request_id) {
                checkProgress(response.data.request_id);
            }
        } catch (error) {
            if (error.response && error.response.status === 401) {
                setSessionExpired(true);
                navigate('/login');
            } else if (error.isAxiosError && !error.response) {
                // This means it's a network error
                alert("Unable to connect to the server. Please check your connection and try again.");
            } else {
                alert("Something went wrong. Try Again!");
            }            
        }
    };
    const [timerInitialized, setTimerInitialized] = useState(false);
    const remainingTimeRef = useRef(null);
    const checkProgress = async (requestId) => {
        let checkInProgress = true;
        const check = async () => {
            if (!checkInProgress) {
                return;
            }
           try {
            const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/check_progress/${requestId}`, {
                withCredentials: true
            });
            if (response.status === 404 || response.status === 202) {
                setTimeout(check, 20000);
                return;
            }
            if (response.data.status === 'completed') {
                checkInProgress = false;
                const emailResponse = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/emailget/${requestId}`, {
                    withCredentials: true
                });
                if(emailResponse.data){
                    setMails(emailResponse.data.Generated_mails);
                    setShowPopup(true);
                    setFormSubmitted(true);
                }
                setShowSpinner(false);
                remainingTimeRef.current = null; // Reset the timer initialization state
            } else if (response.data.status === 'failed') {
                console.error('Processing leads failed.');
                alert("Something went wrong. Try again!");
                setShowSpinner(false);
                remainingTimeRef.current = null; // Reset the timer initialization state
            } else if(response.data.status === 'processing') {
                const { Processed_leads, Total_leads, Estimated_time } = response.data;
                const remainingLeads = Total_leads - Processed_leads;
                const remainingTime = (remainingLeads * Estimated_time).toFixed(2);
                if (remainingTimeRef.current === null) {
                    remainingTimeRef.current = remainingTime;
                }
                setSpinnerMessage(`Processed leads: ${Processed_leads}, Remaining time:`);
                setProcessedLeads(Processed_leads);
                setTimeout(check, 20000);
            }
        } catch (error) {
            if (error.isAxiosError && !error.response) {
                // This means it's a network error
                alert("Unable to connect to the server. Please check your connection and try again.");
                checkInProgress = false; // Stop checking progress
            } else {
                console.error('An unexpected error occurred:', error);
                alert("Something went wrong. Try Again!");
                checkInProgress = false; // Stop checking progress
            }
        }
    }
        check();
    };
    
    const renderer = ({ hours, minutes, seconds, completed }) => {
        if (completed) {
            // Render a completed state
            return <span>Please wait!</span>;
        } else {
            // Render a countdown
            return <span>{hours}:{minutes}:{seconds}</span>;
        }
    };
    
    const [currentMailIndex, setCurrentMailIndex] = useState(0);

    const nextMail = () => {
        setCurrentMailIndex(prevIndex => prevIndex + 1 < mails.length ? prevIndex + 1 : prevIndex);
    }

    const prevMail = () => {
        setCurrentMailIndex(prevIndex => prevIndex - 1 >= 0 ? prevIndex - 1 : prevIndex);
    }

    const closePopup = () => {
        setShowPopup(false);
        setMails([]);
        setCurrentMailIndex(0);
    }

    const handleSaveDetails = async () => {


        
        // Create a FormData instance
        let data = new FormData();
    
        // Append the fields to the form data
        Object.keys(formData).forEach(key => {
            data.append(key, formData[key]);
        });

        if (!formData.USP || !formData.offer || !formData.Company_Name || !formData.Owner_Name || 
            !formData.Service || !formData.Customer || !formData.Industry) {
            alert('Please fill out all the fields.');
            return;
        }

        if (!/^\d{10}$/.test(formData.Phone_number)) {
            alert('Please enter a valid 10-digit phone number.');
            return;
        }

        const urlPattern = new RegExp('^(https?:\\/\\/)?' + // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
        '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
        if (!urlPattern.test(formData.Website) || !urlPattern.test(formData.Consultation_link)) {
            alert('Please enter a valid URL for the website and consultation link.');
            return;
        }
    
        // Make the API call
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/clients`, data, {
                withCredentials: true
            });
    
            if (response.status === 200) {
                console.log("Data saved successfully");
                alert("Data saved successfully!");
            } else {
                console.error("Data could not be saved");
            }
        } catch (error) {
            alert(error)
            console.error("An unexpected error occurred:", error);
            alert("Something went wrong. Try again!");
        }
    };
    const [mailsGenerated, setMailsGenerated] = useState(0);
    const [maxMails, setMaxMails] = useState(1); // default to 1 to avoid division by zero

    useEffect(() => {
        const checkSession = async () => {
            try {
                const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/check_auth`, { withCredentials: true });

                if (res.status === 200) {
                    // Set the mailsGenerated and maxMails state variables
                    const mailsGeneratedNum = Number(res.data.user.mailsGenerated);
                    const maxMailsNum = Number(res.data.user.maxMails);
                    if (!isNaN(mailsGeneratedNum) && !isNaN(maxMailsNum)) {
                        setMailsGenerated(mailsGeneratedNum);
                        setMaxMails(maxMailsNum);
                    } 

                } else {
                    setSessionExpired(true);
                    navigate('/login');
                }
            } catch (error) {
                console.error('An error occurred:', error);
                setSessionExpired(true);
                navigate('/login');
            }
        };
    
        checkSession();
    }, []);
    // Rest of your Client component...

    const [isNavVisible, setIsNavVisible] = useState(false);



    const navRef = useRef(null);  // Create a reference to your nav panel

useEffect(() => {
    const handleClickOutsideNav = (event) => {
        if (navRef.current && !navRef.current.contains(event.target)) {
            setIsNavVisible(false);
        }
    }

    // Add the event listener when the component mounts
    document.addEventListener('mousedown', handleClickOutsideNav);

    // Clean up the event listener on component unmount
    return () => {
        document.removeEventListener('mousedown', handleClickOutsideNav);
    }
}, []);

const nextTemplate = () => {
    if (currentTemplateIndex < templates.length - 1) {
        setCurrentTemplateIndex(currentTemplateIndex + 1);
    }
};

const prevTemplate = () => {
    if (currentTemplateIndex > 0) {
        setCurrentTemplateIndex(currentTemplateIndex - 1);
    }
};


    const percentageUsed = (mailsGenerated / maxMails) * 100;
    const percentageRemaining = 100 - percentageUsed;

    
    
    return (
        <div className="client">
         <div className={`overlay ${showSpinner ? 'show' : ''}`}></div>
        <div className={`spinner-container ${showSpinner ? 'show' : ''}`}>
            <div className="spinner"></div>
        </div>
        <p className={`spinner-text ${showSpinner ? 'show' : ''}`}>
            {spinnerMessage}
            {showSpinner && remainingTimeRef.current && (
                <Countdown
                    date={Date.now() + remainingTimeRef.current * 1000}
                    renderer={renderer}
                />
            )}
        </p>
        <div/>
            {sessionExpired && (
                <div className="session-expired-popup">
                    <p>Session expired. Please log in again.</p>
                </div>
            )}
            <Header />
            <div className="user-menu-container">
                {user && <UserMenu user={user} />}
            </div>
            <button className="nav-toggle" onClick={() => setIsNavVisible(!isNavVisible)}>☰</button> {/* moved up */}
            <div className="panel-container">
            <div ref={navRef} className={`nav-panel ${isNavVisible ? 'nav-visible' : ''}`}>
            <div className="button-container1">
                <button onClick={() => {setPanel('one'); setIsNavVisible(false);}}>
                    <FaMailBulk color="#4CAF50" /> Email Wizard
                </button>
                <button onClick={() => {setPanel('two'); setIsNavVisible(false);}}>
                    <FaDigitalTachograph color="#2196F3" /> Template Generator
                </button>
                <button onClick={() => {setPanel('three'); setIsNavVisible(false);}}>
                    <FaChartBar color="#FFC107" /> Analytics
                </button>
                <button onClick={() => {setPanel('four'); setIsNavVisible(false);}}>
                    <FaEnvelope color="#E91E63" /> Generated mails
                </button>
                <button onClick={() => {setPanel('five'); setIsNavVisible(false);}}>
                    <FaCalendarAlt color="#9C27B0" /> Schedule
                </button>
            </div>
            <span className="subscription-text">{maxMails - mailsGenerated}/{maxMails} mails remaining</span>
            <div className="subscription-card">
                <div className="battery-body">
                <div className="battery-level" style={{'--percentage-used': `${percentageRemaining}%`}}></div>
                </div>
                <div className="battery-tip"></div>
            </div>
                </div>
                

                <div className="main-content">
                    {panel === 'one' && <PanelOne formData={formData} templates={templates} nextTemplate={nextTemplate} prevTemplate={prevTemplate} handleTemplateSelect={handleTemplateSelect} setShowTemplateModal={setShowTemplateModal} showTemplateModal={showTemplateModal}  selectedTemplateIndex={selectedTemplateIndex} handleInputChange={handleInputChange} handleFileUpload={handleFileUpload} currentTemplateIndex={currentTemplateIndex} handleFormSubmit={handleFormSubmit} handleSaveDetails={handleSaveDetails} handleSendMail={handleTemplateModalOpen} handleFinalSend={handleFinalSend}/>}
                    {panel === 'two' && <PanelTwo />}
                    {panel === 'three' && <PanelThree />}
                    {panel === 'four' && <PanelFour templates={templates} nextTemplate={nextTemplate} prevTemplate={prevTemplate} currentTemplateIndex={currentTemplateIndex}/>}
                    {panel === 'five' && <PanelFive/>}
                </div>
               

            </div>
            {showPopup && (
                <div className="popup">
                    <div className="button-cont">
                        <button onClick={closePopup}>Close</button>
                        <button onClick={prevMail}>Prev</button>
                        <button onClick={nextMail}>Next</button>
                    </div>
                    <p>{mails[currentMailIndex]}</p>
                </div>
            )}
        </div>
    );
};

export default Client;