from api.v1 import route_auth
from api.v1 import route_exercise
from api.v1 import route_user
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(router=route_user.router, prefix="/users", tags=["Users"])
api_router.include_router(
    router=route_exercise.router, prefix="/exercises", tags=["Exercises"]
)
api_router.include_router(router=route_auth.router, prefix="/auth", tags=["auth"])
