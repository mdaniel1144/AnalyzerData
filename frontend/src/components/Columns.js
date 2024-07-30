import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Columns.css';

const Columns = ({columns , setCopyCol , primaryKey , foreignKey}) => {

    const [isOpenColumns , setIsOpenColumns] = useState(false)
    const [copyColumns , setcopyColumns] = useState()


    useEffect(() => {
        if(columns){
            setcopyColumns(columns)
        }
      }, [columns]);


    const handelChangeisOpenColumns = () =>{
        setIsOpenColumns(!isOpenColumns)
    }

    const handelSelectValueTypeCol = (event , index) =>{
        const newCopyColumns = [...copyColumns];
        newCopyColumns[index].valueType = event.target.value
        setcopyColumns(newCopyColumns)
        setCopyCol(copyColumns)
    }

    const handelRemoveColumn = (index) =>{
        const newArray = [...copyColumns.slice(0, index), ...copyColumns.slice(index + 1)];
        setcopyColumns(newArray)
        setCopyCol(newArray)
    }

    return (
        <div className='columns-description-container'>
            <table>
                <thead>
                <tr>
                    <td><label>Columns</label></td>
                    <td colSpan={2}><button type='button' className= {`columns-open-button ${isOpenColumns? 'open': ''}`} onClick={handelChangeisOpenColumns}>V</button></td>
                </tr>
                </thead>
                <tbody className={`columns-list-description-container ${isOpenColumns? 'open': ''}`}>
                {copyColumns?
                    (copyColumns.map((col, colIndex) => (
                        <tr key={colIndex}>
                            <td>
                                {col.name}
                                {col.name === primaryKey? <img src="./images/key.png" alt="Primary Key Icon" className='image-key'/> : null}
                                {col.name === foreignKey? <img src="./images/key4.png" alt="Foreign Key Icon" className='image-key'/> : null}
                            </td>
                            <td>
                            {<select className='columns-select' name={`type${colIndex}`} id={`type${colIndex}`} value={col.valueType} onChange={(e) => handelSelectValueTypeCol(e,colIndex)}>
                                <option value="int64">int64</option>
                                <option value="category">category</option>
                                <option value="object">object</option>
                                <option value="float64">float64</option>
                            </select>}
                            </td>
                            <td>{col.name !== primaryKey && <img src='/images/removeIcon.png' className='remove-button' onClick={(e) => handelRemoveColumn(colIndex)}/>}</td>
                        </tr>
                    )))
                    :
                    (null)
                }
                </tbody>
            </table>
    </div>
  )
};

export default Columns;