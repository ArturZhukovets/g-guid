import React, {useState} from 'react';
import './css/index.css';
import Header from './components/Header'
import ExercisesList from './components/ExercisesList'

import ExerciseForm from './components/ExerciseForm';

function App() {
  // Emulating exercises from DB
  const [exercises, setExercises] = useState([
    {id:1, title: "First Exercise", body: "Super exercise on your legs"},
    {id:2, title: "Second Exercise", body: "Super exercise on your body"},
    {id:3, title: "Third Exercise", body: "Super exercise on your arms"},
    {id:4, title: "Fourth Exercise", body: "Super exercise on your chest"},
    {id:5, title: "Fifth Exercise", body: "Super exercise on your back"},
  ])

  // Функция - callback, которую передаём как аргумент внутрь компонента.
  // Внутри самого компонента данную функцию вызываем с новым упр.
  const createExercise = (newExercise) => {
    setExercises([...exercises, newExercise])
  }

  // Функция - callback для удаления упр. логика такая же:
  // Передаём внутрь компонента и вызываем внутри самого компонента
  const removeExercise = (exercise) => {
	setExercises(exercises.filter(ex => ex.id !== exercise.id))
  }

    return (
        <div className="App">
            <Header title="This is g-guid header!"/>
            <div className='container'>
              	<ExerciseForm create={createExercise}></ExerciseForm>
				{
					exercises.length
					? <ExercisesList
						exercises={exercises}
						title="List of exercises of the current user"
						remove={removeExercise}
					/>
					: <h2 style={{textAlign: 'center', margin: '20px'}}>Current user has no exercises</h2>
				}


            </div>
        </div>
      );
}

export default App;
