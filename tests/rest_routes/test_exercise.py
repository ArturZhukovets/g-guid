"""
This module provide tests for api endpoints.
Write only  api endpoint tests here...
"""
from api.v1.route_exercise import router
from db.models.exersices import Exercise
from tests.utils.exercise import create_random_exercise

EXERCISES_ENDPOINT = "/exercises"


def test_fetch_created_exercise(client, db_session, user):
    exercise = create_random_exercise(db_session, user_id=user.id)
    assert exercise.id == 1
    response = client.get("/exercises/1")
    assert response.status_code == 200
    assert response.json()["title"] == exercise.title


def test_exercise_create(client, db_session, user):
    user_id = str(user.id)
    create_path_url = (
        EXERCISES_ENDPOINT
        + router.url_path_for("exercise_create")
        + f"?user_id={user_id}"
    )
    data = {
        "title": "test",
        "description": "some-test-description",
        "category": "Legs",
    }
    response = client.post(create_path_url, json=data)
    assert response.status_code == 201
    assert (
        db_session.query(Exercise).filter(Exercise.user_id == int(user_id)).count() == 1
    )
