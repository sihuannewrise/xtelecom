from fastapi import FastAPI

from telecom.core.config import settings

app = FastAPI(title=settings.app_title, docs_url="/swagger")


@app.get("/")
def read_root():
    return {"hello": "telecom"}


@app.get("/config", tags=["settings"])
def read_config():
    return {"model_dump": settings().model_dump()}
