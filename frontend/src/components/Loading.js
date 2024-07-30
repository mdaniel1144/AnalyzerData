import React , {useEffect , useState} from 'react';
import './Loading.css';

const Loading = () => {

  const [nameGif , setNameGif] = useState(1) 

  useEffect(()=>{
    const randomLoding = Math.floor(Math.random() * 4) + 1
    setNameGif( "/images/loading"+randomLoding+".gif")
  },[])

  return (
    <div className='loading-container'>
        <img src={nameGif} alt="loading ... " />
        <label>Loading...</label>
    </div>
  );
};

export default Loading;
