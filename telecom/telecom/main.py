from fastapi import FastAPI
from telecom.core.config import settings

xtelecom = FastAPI(
    title=settings.app_title,
    docs_url="/swagger",
    redoc_url=None,
)


@xtelecom.get("/")
def read_root() -> dict[str, str]:
    return {"hello": "telecom"}


@xtelecom.get("/config", tags=["settings"])
def read_config() -> dict[str, str]:
    return {"model_dump": "Settings().model_dump()"}
