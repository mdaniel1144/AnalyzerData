import logo from './logo.svg';

import React, { useEffect, useState } from 'react';
import TablePreview from './components/TablePreview';
import QueryResult from './components/QueryResult';
import Message from './components/Message';
import Sidebar from './components/SidebarMenu/Sidebar';
import Summary from './components/Summary';
import OpeningPage from './components/OpeningPage';
import './App.css';

function App() {

  const [indexTab , setIndexTab] = useState(0)
  const [listData, setListData] = useState([])  ///the current
  const [listName , setListName] = useState([])
  const [interstingCol , setinterstingCol] = useState('')
  const [message , setMessage] = useState('') 
  const [page , setPage] = useState(0)
  const [query , setQuery] = useState('')

  const pageChanging = (pageNUmber) =>{
    setPage(pageNUmber)
  }
  const QuaryChanging = (query) =>{
    setQuery(query)
    setPage(3)
  }

  const indexTabChanging = (index) =>{
    setIndexTab(index)
    console.log("you chose "+index+" tab")
  }

  const handeChangelListData = (action , newData , index) =>
  {
    const newListData = [...listData]

    if (indexTab >=0 && indexTab <listData.length){
      if (action === "remove"){
        newListData.splice(index, 1);
        setListData(newListData);
        if (indexTab -1 >=1)
          setIndexTab(indexTab-1)
        else
          setIndexTab(0)
      }
    }
    if (action === "insert"){
      newListData.push(newData)
      setIndexTab(indexTab+1)
      setListData(newListData)
      console.log("i insert new "+indexTab)
    }
    if (action === "update")
    {
      console.log("i update "+indexTab)
      newListData[indexTab] = newData
      setListData(newListData)
    }
    if(newListData){
      const newlistName = newListData.map(item => {
        if (item) 
          return item.name;
        else
        return ""})
      setListName(newlistName)
    }
  }

  const interstingColChanging = (col) =>{
    setinterstingCol(col)
  }
  const messageChanging = (response) =>{
    setMessage(response)
  }

  useEffect(()=>{
    if(listData.length === 0){
        setPage(0)
        setIndexTab(0)
        setListName([])
    }
  } , [listData])




  return  (
    <div className="App">
      <Sidebar page={page} listData={listData} setPage={pageChanging} setListData={setListData} setMessage={messageChanging}  setinterstingCol={setinterstingCol} setChangelListData={handeChangelListData} QuaryChanging={QuaryChanging} />
      {message && 
          <Message message={message} setMessage={messageChanging} />
      }
      {page === 0? (<OpeningPage />) : null}
      {page === 1? (<TablePreview data={listData[indexTab]} setPage={pageChanging} setinterstingCol={interstingColChanging} setMessage={messageChanging} indexTab={indexTab}  setIndexTab={indexTabChanging} setChangelListData={handeChangelListData} listName={listName}/>) : null}
      {page === 2? (<Summary data={listData[indexTab]} interstingCol={interstingCol} setMessage={messageChanging} setPage={pageChanging}/>): null}
      {page === 3? (<QueryResult listData={listData} query={query} setMessage={messageChanging} setPage={pageChanging}/>): null}
    </div>
  );
}

export default App;
