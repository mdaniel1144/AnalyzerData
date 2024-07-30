import React, { useEffect, useState } from 'react';
import Columns from './Columns';
import axios from 'axios';
import './Description.css';

const Description = ({data , setPage , setChangelListData , setMessage}) => {

    const [isEdit , setEditMode] = useState({mode: false , lable : "Edit"})
    const [col , setCol] = useState()
    const [primaryKey , setPrimaryKey] = useState()
    const [primaryKeyCopy , setPrimaryKeyCopy] = useState()
    const [foreignKey , setForeignKey] = useState()
    const [foreignKeyCopy , setForeignKeyCopy] = useState()
    const [reference , setReference] = useState()
    const [name , setName] = useState() 

    useEffect(() => {
        if(data != null){
            setName(data.name)
            setPrimaryKey(data.primaryKey)
            setPrimaryKeyCopy(data.primaryKey)
            setForeignKey(data.foreignKey)
            setForeignKeyCopy(data.foreignKey)
            setReference(data.reference)
            setCol(data.columns.map(column => ({ ...column })))
            console.log("data change description")
        }
        else{
            setName("undefined")
            setPrimaryKey("")
            setPrimaryKeyCopy("")
            setForeignKey("")
            setForeignKeyCopy("")
            setReference("")
            setCol(null)
        }
      }, [data]);


    const handelSaveChangeInData = async (event) =>{
        
        if(name === ""){
            setMessage({"type": "error" , "content" : "Your Name table is None"})
        }
        else if (!col.some(column => column.name === primaryKey)){
            setMessage({"type": "error" , "content" : "Is not exist Primary Key"})
        }
        else if (primaryKey === foreignKey){
            setMessage({"type": "error" , "content" : "Primary Key can not be like Foreign Key"})
        }
        else if ("" !== foreignKey && !col.some(column => column.name === foreignKey)){
            setMessage({"type": "error" , "content" : "Is not exist Foreign Key"})
        }
        else
        {
            const newData = await checkIsTypeIsOk()
            if (newData.table != null){
                setMessage(newData.message)
                setChangelListData("update" , newData.table , 0)
                setEditMode({mode: false , lable: "Edit"})
            }
            else
            setMessage(newData.message)
        }
        setEditMode({mode: false , lable: "Edit"})
    }

    const  checkIsTypeIsOk = async () =>{
        const payload = {
            data: data,
            newCols: col,
            name : name,
            primaryKey : primaryKey,
            foreignKey: foreignKey,
            reference: reference
        }
        const result = await axios.post('http://localhost:8000/checkSetting/', payload, 
        {headers: {'Content-Type': 'application/json'}},);

        return result.data
    }


    const handelChangeEditMode = (event) =>{
        if(isEdit.mode){
            setEditMode({mode: false , lable: "Edit"})
            setName(data.name)
            setPrimaryKey(data.primaryKey)
            setPrimaryKeyCopy(data.primaryKey)
            setForeignKey(data.foreignKey)
            setForeignKeyCopy(data.foreignKey)
            setCol(() => data.columns.map(column => ({ ...column })))
            }
        else
            setEditMode({mode: true , lable: "Cancel"})
    }

    const handelFixData = async (event) =>{
        const payload = {
            data: data,
            primaryKey : primaryKey,
            foreignKey: foreignKey,
        }
        const result = await axios.post('http://localhost:8000/fixKeys/', payload, 
        {headers: {'Content-Type': 'application/json'}},);

        if (result.data.table){
            setMessage(result.data.message)
            setChangelListData("update" , result.data.table , 0)
        }
        else
            setMessage(result.data.message)
    }

    const handelChangeForeignKey= (event) => {
        if(col.some(column => column.name === event.target.value.trim())){
            setForeignKeyCopy(event.target.value.trim())}
        setForeignKey(event.target.value.trim())
    }

    const handelChangePrimaryKey = (event) => {
        if(col.some(column => column.name === event.target.value.trim())){
            setPrimaryKeyCopy(event.target.value.trim())}
        setPrimaryKey(event.target.value.trim())
    }

    const handelSetName = (event) =>{
        setName(event.target.value.trim())
    }
    const handelSetReference = (event) =>{
        setReference(event.target.value.trim())
    }

    const hanedlCopyColumns = (updateColummns) =>{
        setCol(updateColummns)
    }


    const handelButtonFixData = async (event) =>{
        event.preventDefault()
        if(data)
            setPage(2)
        else
            setMessage({"type": "error" , "content" : "Your table is Empty"})
    }
    
    return (
        <div className='preview-description'>
            <h2>Description</h2>
            <table className='table-preview-description'>
            <tr>
                <td><label>Name</label></td>
                <td>
                    {isEdit.mode?  
                        (<input type="text" className='text-input' value={name} onChange={handelSetName} />)
                    :
                        (name)
                    }
                </td>
            </tr>
            <tr>
                <td><label>Primary Key</label></td>
                <td>
                    {isEdit.mode?  
                        (<input type="text" className='text-input' value={primaryKey} onChange={handelChangePrimaryKey} />)
                    :
                        (primaryKey)
                    }
                </td>
            </tr>
            <tr>
                <td><label>Foreign Key</label></td>
                <td>
                    {isEdit.mode?  
                        (<input type="text" className='text-input' value={foreignKey} onChange={handelChangeForeignKey} />)
                    :
                        (foreignKey)
                    }
                </td>
            </tr>
            <tr>
                <td><label>Reference</label></td>
                <td>
                    {isEdit.mode?  
                        (<input type="text" className='text-input' value={reference} onChange={handelSetReference} />)
                    :
                        (reference)
                    }
                </td>
            </tr>
            <tr>
                <td><label>Rows</label></td>
                {data && (<td>{data.size[0]}</td>)}
            </tr>
            {isEdit.mode?
                (<tr><td colSpan={2}><Columns columns={col} primaryKey={primaryKeyCopy} foreignKey={foreignKeyCopy} setCopyCol={hanedlCopyColumns}/></td></tr>)
                    :
                (<tr><td><label>Columns</label></td>{data && (<td>{data.size[1]}</td>)}</tr>)
            }   
        </table>
        {data != null && (<button type='button' className={`submit-button ${isEdit.mode? "yes" : ""}`} onClick={handelChangeEditMode}>{isEdit.lable}</button>)}
        {data != null && (<button type='button' className='submit-button' onClick={handelFixData}>Fix Data</button>)}
        {isEdit.mode && data? 
            (<button className='submit-button' type='button' onClick={handelSaveChangeInData}>Save</button>)
            :
            (null)
        }

    </div>
  )
};

export default Description;