import React, { useEffect ,useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes , faChevronRight } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import './SidebarSummary.css';

const SidebarSummary = ({listData, setinterstingCol ,setPage}) => {

    const [isOpenSummary, setIsOpenSummary] = useState(false);
    const [interstingColCopy , setinterstingColCopy] = useState('')


    const handleInterstingColChange = (event) =>{
      event.preventDefault()    
      setinterstingColCopy(event.target.value.trim())
    }


    const toggleSummary = () => {
      setIsOpenSummary(!isOpenSummary);
    };
    
    const handleMakeSummary = () => {
      setinterstingCol(interstingColCopy)
      setPage(2)
    }

    return (
      <div className= {`sidebar-summary-container ${isOpenSummary ? 'open' : 'closed'}`}>
        <div className='sidebar-summary-menu-container'>

        <h1>Make Summary</h1>
        <div className='summary-decription-container'>
            <label>Please enter your intersting Column, in the current table</label>
            <input type="text" id="primaryKey" onChange={handleInterstingColChange} className="text-input" />
          <button type='button' onClick={handleMakeSummary} className="submit-button">Summary</button>
        </div>

        </div>       
        <button className="sidebar-summary-container-button" onClick={toggleSummary}>
      <FontAwesomeIcon icon={isOpenSummary ? faTimes : faChevronRight} 
          className={`sidebar-button-icon ${isOpenSummary ? 'rotate' : 'reset'}`}/>
    </button>
      </div>
    );
  };

export default SidebarSummary;

