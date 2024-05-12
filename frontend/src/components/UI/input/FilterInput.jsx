import React from 'react'
import classes from "./FilterInput.module.css"

const FilterInput = (props) => {
    return (
        <div className={classes.filterInput}>
            <label htmlFor={props.id}>{props.label}</label>
            <input {...props}/>
        </div>
        );
}

export default FilterInput;