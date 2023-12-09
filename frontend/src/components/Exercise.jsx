import React from 'react'
import DefaultButton from './UI/button/DefaultButton'

const Exercise = (props) => {
    return (
        <div className="exercise">
            <div className='exercise_content'>
                <strong>{props.number}. {props.exercise.title}</strong>
                <div>
                    {props.exercise.body}
                </div>
            </div>
            <div className='deleteExersize'>
                <DefaultButton
                onClick={() => props.remove(props.exercise)}>
                    Delete exercise
                </DefaultButton>
            </div>
        </div>
    )
}

export default Exercise
