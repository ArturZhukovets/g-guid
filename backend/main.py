import uvicorn
from api.base import api_router
from core.config import settings
from fastapi import FastAPI


def include_router(_app) -> None:
    _app.include_router(api_router)


def create_tables() -> None:
    # Base.metadata.create_all(bind=engine)
    pass


def start_application() -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(_app=_app)
    return _app


# ================================================================================== #


app = start_application()


@app.get("/")
def hello_api():
    return {"msg": "Hello FastAPI🚀"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
