import React from 'react'
import classes from "./DefaultInput.module.css"

const DefaultInput = (props) => {
    return (
        <input className={classes.defaultInput} {...props}/>
        );
}

export default DefaultInput
