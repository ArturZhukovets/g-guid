import React from 'react'
import Exercise from './Exercise'

const ExercisesList = ({exercises, title, remove}) => {
    return (
        <div className='exercises_list'>
                <div>
                  <h2 style={{fontSize: '40px', margin: '10px'}}>{title}</h2>
                </div>

                {
                    exercises.map((exercise, index) =>
                    <Exercise number={index + 1} exercise={exercise} key={exercise.id} remove={remove}/>
                    )
                }

        </div>
    )
}

export default ExercisesList
