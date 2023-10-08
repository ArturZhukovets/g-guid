from fastapi import APIRouter

from api.v1 import route_user, route_exercise


api_router = APIRouter()
api_router.include_router(router=route_user.router, prefix="/users", tags=["Users"])
api_router.include_router(router=route_exercise.router, prefix="/exercises", tags=["Exercises"])

