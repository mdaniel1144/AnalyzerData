import React, { useEffect ,useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes , faChevronRight } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import './SqlDatabase.css';

const SqlDatabase = ({QuaryChanging , listData ,setMessage}) => {

    const [query , setQuery] = useState("")
    const [isOpenSql, setIsOpenSql] = useState(false);
    const [mode , setMode] = useState(false)

    const handleQueryChange = (event) =>{
      setQuery(event.target.value)
    }

    const handleFormMode = (event) =>{
      setMode(!mode)
    }
    const handleQuaryChanging = async (event) =>{
      event.preventDefault()
      if(query != "")
        QuaryChanging(query)
      else
        setMessage({'type': 'error' ,'content': "Your Query is empty"})
    }

    const toggleSql = () => {
      setIsOpenSql(!isOpenSql);
    };
    
    const handleDownload = async () => {
      try {
        const payload = {
          listData: listData
        }
        const response = await axios.post('http://localhost:8000/BuildDatabase/', payload,
         {headers: { 'Content-Type': 'application/json' },
         responseType: 'blob' });

        if(response.status === 200){

          const blob = new Blob([response.data], { type: 'application/octet-stream' });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');

          a.style.display = 'none';
          a.href = url;
          a.download = 'database.sql';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        }
        else
          throw new Error("something is worng in the service")

      } 
      catch (error) {
        if(error.response){
          setMessage({'type': 'error' ,'content': error.response.data.message})
        }
        else
          console.error(error)
      }
    };


    return (
      <div className= {`sql-container ${isOpenSql ? 'open' : 'closed'}`}>
        <div className='sql-menu-container'>

          <h1>Make Database</h1>
          <div className='sql-method-mode-container'>
            <div className={`sql-method-mode ${mode ? 'quary' : 'build'}`} onClick={handleFormMode}>
              <label>{mode? "Quary" : "Build"}</label>
            </div>
          </div>
          {mode? 
            ( <div className="sql-query-container">
              <label>Please enter a SQL Quary</label>
                <textarea type="text" id="query" value={query} onChange={handleQueryChange} />
                <button onClick={handleQuaryChanging}><img src="/logo192.png" alt="logo"/></button>
              </div>)
            :
            (<button onClick={handleDownload}>Make Database</button>)
          }

        </div>       
        <button className="sql-container-button" onClick={toggleSql}>
      <FontAwesomeIcon icon={isOpenSql ? faTimes : faChevronRight} 
          className={`sidebar-button-icon ${isOpenSql ? 'rotate' : 'reset'}`}/>
    </button>
      </div>
    );
  };

export default SqlDatabase;

