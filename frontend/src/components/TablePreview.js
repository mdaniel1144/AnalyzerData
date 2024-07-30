import React, { useEffect, useState } from 'react';
import Loading from './Loading';
import './TablePreview.css'; // Import your CSS file
import Description from './Description';
import Tab from './tab';



const TablePreview = ({indexTab , setIndexTab , data, listName , setPage  , setMessage , setChangelListData}) => {

    const [loading , setLoading] = useState(true)
    
    useEffect(() => {
        if(data){
            setLoading(true)
            setTimeout(() => {
                setLoading(false); // Set loading to false after some delay (simulating data fetch)
            }, 2000);
        } // Simulating a 2 second delay, replace with your actual data fetching logic
    }, [data]);

    const stylex={display: "inline-block"}

    return (
        <div className='preview-container'>
        <h1>Preview Dataset</h1>
        <Description data={data} setChangelListData={setChangelListData} setPage={setPage} setMessage={setMessage} />
        <div className='table-tab-preview-container'>
            <Tab style={stylex} indexTab={indexTab} setIndexTab={setIndexTab} listName={listName} setChangelListData={setChangelListData}/>
            <div className='table-preview-container'>
            {loading? 
                    (<Loading />) 
                :
                    (<div>
                        {data && (<table border="1" className='table-preview'>
                        <thead>
                            <tr>
                                {data.columns.map((column, index) => (
                                <th key={index}>{column.name}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {data.rows.map((row, rowIndex) => (
                            <tr key={rowIndex}>
                                {row.map((cell, cellIndex) => (
                                <td key={cellIndex}>{cell}</td>
                                ))}
                            </tr>
                            ))}
                        </tbody>
                        </table>)}
                    </div>       
            )}
            </div>
        </div>
        </div>
    );
};

export default TablePreview;