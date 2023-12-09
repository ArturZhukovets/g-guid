import React, {useState} from 'react'
import DefaultButton from './UI/button/DefaultButton'
import DefaultInput from './UI/input/DefaultInput'
import DefaultTextarea from './UI/textarea/DefaultTextarea'


const ExerciseForm = ({create}) => {

    const [exercise, setExercise] = useState({title: '', body: ''})

    const addNewExercise = (e) => {
        e.preventDefault();
        const newExercise = {
            ...exercise, id: Date.now()
        }
        create(newExercise)   // Вызываем функцию для создания нового упр.
        setExercise({title: '', body: ''})

      }

    return (
        <form>
            <DefaultInput
            type='text'
            placeholder='Exercise title'
            value={exercise.title}
            onChange={e => setExercise({...exercise, title: e.target.value})}
            />
            <DefaultTextarea
            type='text'
            placeholder='Exercise Description'
            value={exercise.body}
            onChange={e => setExercise({...exercise, body: e.target.value})}
            />
            <DefaultButton onClick={addNewExercise} > Submit</DefaultButton>
      </form>
    )
}

export default ExerciseForm
