import React, { useEffect, useState } from 'react';
import Loading from './Loading';
import './QueryResult.css'; // Import your CSS file
import axios from 'axios';


const QueryResult = ({listData , query ,setMessage, setPage}) => {

    const [loading , setLoading] = useState(true)
    const [results , setResults] = useState(null)
    
    const getQueryResults= async () => {
        try
        {
            const payload = {
                listData: listData,
                query: query
            }
            const result = await axios.post('http://localhost:8000/makeQuery/', payload, 
            {headers: {'Content-Type': 'application/json'}});

            if(result.status === 200){
                setResults(result.data.results)
                setMessage({'type': 'succses' ,'content':"Succsesfull get Query"})
            }
            else
                throw new Error("something is worng in the service")
        } 
        catch (error) {
            if(error.response){
                const result = error.response
                setPage(1)
                setMessage({'type': 'error' ,'content': result.data.message})
            }
            else
                console.error(error)

        }
    }

    useEffect(() => {
        getQueryResults();
        setLoading(true)
        // Simulate an async data fetch (replace with actual fetch logic if needed)
        setTimeout(() => {
        setLoading(false); // Set loading to false after some delay (simulating data fetch)
            }, 3000); // Simulating a 2 second delay, replace with your actual data fetching logic
    }, [query]);


    if(!results)
        return null

    return (
        <div className='queryResult-container'>
        <h1>Query Result</h1>
        {loading? 
            (
                <div className='queryResult-container'><Loading/></div>
            ) 
            : 
            (
                <div className='queryResult-table-container'>
                {loading? 
                    (<Loading />) 
                :
                    (<div>
                        {results  && results.length > 0?  (<table className='queryResult-table-preview'>
                        <thead>
                            <tr>
                                {Object.keys(results[0]).map((col) => (
                                <th>{col}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {results.map((row, rowIndex) => (
                            <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'even' : 'odd'}>
                                {Object.values(row).map((cell, cellIndex) => (
                                <td key={cellIndex}>{cell}</td>
                                ))}
                            </tr>
                            ))}
                        </tbody>
                        </table>)
                        :
                        (<div>No results found</div>)
                        }
                    </div>       
            )}
            </div>
        )}
    </div>
    );
};

export default QueryResult;