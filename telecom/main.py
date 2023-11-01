from fastapi import FastAPI
from telecom.core.config import settings

app = FastAPI(title=settings.app_title, docs_url="/swagger")


@app.get("/config", tags=["settings"])
def read_config():
    print(settings.model_dump())
    return {"model_dump": "Settings().model_dump()"}
