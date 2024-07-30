import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes , faChevronRight } from '@fortawesome/free-solid-svg-icons';
import UploadTableForm from '../UploadTableForm';
import SqlDatabase from './SqlDatabase';
import SidebarSummary from './SidebarSummry'
import './Sidebar.css';



const Sidebar = ({page ,listData ,setListData , setPage , setMessage , setChangelListData ,setinterstingCol , QuaryChanging}) => {

    const [isOpenUpload, setIsOpenUpload] = useState(false);


    const toggleSidebar = () => {
      setIsOpenUpload(!isOpenUpload);
    };



    return (
      <div>
      <div className={`sidebar ${isOpenUpload ? 'open' : 'closed'}`}>
        <div className='sidebar-menu'>
          <UploadTableForm setListData={setListData} setPage={setPage} setMessage={setMessage} setChangelListData={setChangelListData}/>
        </div>
            <button className="sidebar-button" onClick={toggleSidebar}>
            <FontAwesomeIcon 
                icon={isOpenUpload ? faTimes : faChevronRight} 
                className={`sidebar-button-icon ${isOpenUpload ? 'rotate' : 'reset'}`}
                />
        </button>
      </div>
      {page !== 0 && <SqlDatabase QuaryChanging={QuaryChanging} listData={listData} setMessage={setMessage}/>}
      {page !== 0 && <SidebarSummary setPage={setPage} listData={listData} setinterstingCol={setinterstingCol}/>}
    </div>
    );
  };

export default Sidebar;

