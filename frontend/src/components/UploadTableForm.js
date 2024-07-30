import React, { useState } from 'react';
import axios from 'axios';
import './UploadTableForm.css'; // Import your CSS file

const UploadTableForm = ({setPage, setListData , setMessage , setChangelListData}) => {
    const [isOpen , setIsOpen] =  useState(false);
    const [file, setFile] = useState(null);
    const [mode , setMode] = useState(false)
    const [textJson , setTextJSON] = useState('')
    const [name , setName] = useState('')
    const [primaryKey, setPrimaryKey] = useState('');
    const [foreignKey, setForeignKey] = useState('');
    const [reference, setReference] = useState('');

    const handleReset = (event) =>{
        setTextJSON('')
        setName('')
        setPrimaryKey('')
        setPage(0)
        setFile(null)
        setListData([])
        setForeignKey('')
        setReference('')
        console.log("Make Restart to app")
    }

    const handleFormMode = (event) =>{
        setMode(!mode)
    }
    const handleIsOpen = (event) =>{
        setIsOpen(!isOpen)
    }
    const handleNameChange = (event) =>{
        setName(event.target.value)
    }
    const handleForeignKeyChange = (event) =>{
        setForeignKey(event.target.value)
    }
    const handleReferenceChange = (event) =>{
        setReference(event.target.value)
    }

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handlePrimaryKeyChange = (event) => {
        setPrimaryKey(event.target.value);
    };
    
    const handleTextareaChange = (event) => {
        setTextJSON(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();

        if ((!file || !primaryKey) && !mode) {
            setMessage({"type" : "error" ,"content": "File or primary key is missing"});
            return;
        }
        if ((!textJson || !primaryKey || !name) && mode) {
            setMessage({"type" : "error" ,"content": "Json, primary key or name is missing"});
            return;
        }
        try {
            let result
            if (mode === false){
                formData.append('file', file);
                formData.append('primaryKey', primaryKey);
                formData.append('foreignKey', foreignKey);
                formData.append('reference', reference);
                result = await axios.post('http://localhost:8000/uploadfile/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
            }
            else
            {
                const payload = {
                    json: textJson,
                    name: name,
                    primaryKey: primaryKey,
                    foreignKey: foreignKey,
                    reference:  reference
               }
                result = await axios.post('http://localhost:8000/uploadJson/', payload, 
                {headers: {'Content-Type': 'application/json'}},);
            }
            console.log("succses make table")
            setPage(1) //-->MOVE to page Preview
            setChangelListData("update" , result.data.table , 0)
            setMessage(result.data.message);
        } catch (error) {
            console.error(error)
            setMessage(error.message);
        }
    };

    return (
        <div className="upload-form-container">
            <form onSubmit={handleSubmit} className="upload-form">
                <button type='reset' className="submit-button" onClick={handleReset}>Restart</button>
                <button type='reset' className="submit-button" onClick={() =>{setPage(1)}}>Back</button>
                <div className="form-group">
                    <h1 htmlFor="file">Make DataFrame</h1>
                    <div className='upload-form-mode-container'>
                        <div className={`upload-form-mode ${mode ? 'file' : 'textarea'}`} onClick={handleFormMode}>
                            <label>{mode? "text" : "file"}</label>
                        </div>
                    </div>
                    {mode ?
                        <div className="upload-form-textarea-continer">
                            <label className="upload-label-text" htmlFor="textarea">Upload Json Text:</label>
                            <textarea type="textarea" id="textarea" value={textJson} onChange={handleTextareaChange} className="textarea-input" rows="5" />
                            <label className="upload-label-text" htmlFor="name">Name</label>
                            <input type="text" id="name" value={name} onChange={handleNameChange} className="text-input" rows="5" />
                        </div>
                        :
                        <div className="upload-form-file-continer">
                            <label className="upload-label-text" htmlFor="file">Upload CSV/Json File:</label>
                                <input type="file" id="file" onChange={handleFileChange} className="file-input" accept=".csv,.json" />
                                {file && 
                                    <div className='file-container'>
                                    {file.type === 'application/json' ? (
                                        <img src="/images/json.jpg" alt="JSON File" />
                                        ) : (
                                        <img src="/images/csv.jpg" alt="CSV File" />
                                        )}
                                    <label className="upload-label-text">{file.name}</label>
                                </div>}
                        </div>
                    }

                </div>
                <div className="form-group">
                    <label className="upload-label-text" htmlFor="primaryKey">Primary Key:</label>
                    <input type="text" id="primaryKey" value={primaryKey} onChange={handlePrimaryKeyChange} className="text-input" />
                </div>

                <div>
                    <section>
                        <button type='button' onClick={handleIsOpen} className={`advance-open-button ${isOpen? 'open':''}`}> &gt; </button>
                        <label>Advance Setting</label>
                    </section>
                    <div className={`advance-option-container ${isOpen? 'open':''}`}>
                        <div className="form-group">
                            <label className="upload-label-text" htmlFor="foreignKey">Foreign Key:</label>
                            <input type="text" id="foreignKey" value={foreignKey} onChange={handleForeignKeyChange} className="text-input" />
                        </div>
                        <div className="form-group">
                            <label className="upload-label-text" htmlFor="reference">Reference:</label>
                            <input type="text" id="reference" value={reference} onChange={handleReferenceChange} className="text-input" />
                        </div>
                    </div>
                </div>

                <button type="submit" className="submit-button">Upload</button>
            </form>
        </div>
    );
};

export default UploadTableForm;