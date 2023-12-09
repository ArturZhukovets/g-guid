import React from 'react'
import classes from "./DefaultTextarea.module.css"

const DefaultTextarea = (props) => {
    return (
        <textarea className={classes.DefaultTextarea} {...props}/>
        );
}

export default DefaultTextarea
