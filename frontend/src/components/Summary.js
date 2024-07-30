import React, { useEffect, useState } from 'react';
import Loading from './Loading';
import './Summary.css'; // Import your CSS file
import axios from 'axios';



const Summary = ({data ,interstingCol , setMessage , setPage}) => {

    const [loading , setLoading] = useState(true)
    const [summary , setSummary] = useState(null)
    
    const getSummary = async () => {
        try
        {
            const payload = {
                 table: data,
                 interstingCol: interstingCol,
            }
            const result = await axios.post('http://localhost:8000/summary/',  payload,
            {headers: {'Content-Type': 'application/json'}},);

            if(result.data.summary){
                setSummary(result.data.summary)
            }
            else
            {
                setPage(1)
            }
            setMessage(result.data.message)
        } 
        catch (error) {
            console.error(error.message)
            setMessage(error.message)
        }
    }

    useEffect(() => {
        getSummary();
        setLoading(true)
        // Simulate an async data fetch (replace with actual fetch logic if needed)
        setTimeout(() => {
        setLoading(false); // Set loading to false after some delay (simulating data fetch)
            }, 4000); 
    }, []);


    if(!summary)
        return (
        <div className='preview-container'>
            <h1>Summary Dataset</h1>
            <div className='summary-container'><Loading/></div>
        </div>
        )

    return (
        <div className='preview-container'>
        <h1>Summary Dataset</h1>
        {loading? 
            (
                <div className='summary-container'><Loading/></div>
            ) 
            : 
            (
                <div>
                    <div className='interstingCol-info-container'>
                        <h1>{summary.name} Summary</h1>
                        <p>{summary.count}</p>
                        <h2>{summary.interstingCol} Description</h2>
                        <ul>
                            {Object.keys(summary.interstingColDescription[Object.keys(summary.interstingColDescription)[0]]).map(key => (
                            <li key={key}><strong>{key}:</strong> {summary.interstingColDescription[Object.keys(summary.interstingColDescription)[0]][key]}</li>
                            ))}
                        </ul>
                    </div>
                    <div className='graphs-container'>
                    <div className='graphs-category-container'>
                        {summary.graphCategory.map((category, index) => (
                            <div className="graph-catgory">
                                <img key={index} className='image-graph' src={`data:image/png;base64,${category}`} alt="Plot" />
                            </div>
                        ))}
                    </div>
                    <div className='graphs-numric-container'>
                        {summary.graphNumric.map((numric, index) => (
                            <div className="graph-numric">
                                <img key={index} className='image-graph' src={`data:image/png;base64,${numric}`} alt="Plot" />
                            </div>
                        ))}
                    </div>
                    </div>
                </div>
        )}
    </div>
    );
};

export default Summary;