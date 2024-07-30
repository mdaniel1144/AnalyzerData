import React, { useEffect, useState } from 'react';
import './tab.css';

const Tab = ({indexTab , setIndexTab , listName , setChangelListData}) => {


    const addTab = () => {
        if (listName.length <5){     
            setChangelListData("insert", undefined , 0)
        }
    };

    const removeTab = (event ,index) => {
        event.stopPropagation()
        setChangelListData("remove", undefined , index)
    };

    const handelChangeIndex = (index) =>{
        setIndexTab(index)
    }

    return (  
        <div className='tab-container'>
                <section className='tab-tables'>
                    {listName.map((name , index) => {
                        if (indexTab === index) {
                            return (
                                <div key={index} className='tab-data-container tab-background' onClick={()=>handelChangeIndex(index)}>
                                    <button className='tab-button' onClick={(e) => removeTab(e , index)}>-</button>
                                    {name}
                                </div>
                            );
                        } else {
                            return (
                                <div key={index} className='tab-data-container' onClick={()=>handelChangeIndex(index)}>
                                    <button className='tab-button' onClick={(e) => removeTab(e , index)}>-</button>
                                    {name}
                                </div>
                            );
                        }
                    })}
                <button className='tab-button-container' onClick={addTab}>+</button>
                </section>
        </div>
  )
};

export default Tab;