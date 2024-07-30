import React, { useState , useEffect } from 'react';

import './Message.css'; // Assuming you have a CSS file for styling

const Message = ({ message , setMessage}) => {

    useEffect(() => {
        const timer = setTimeout(() => {
        setMessage(null)
        //setIsVisible(false);
        }, 3000); // Message disappears after 3 seconds

        return () => clearTimeout(timer);
    }, []); // Empty dependency array ensures this effect runs only once

    return (
        <div className={`message ${message.type === 'error' ? 'error' : 'succses' }`}>
            {message.content}
        </div>
    );
};

export default Message;