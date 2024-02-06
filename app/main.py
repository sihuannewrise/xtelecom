from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from telecom.api.v1.routers import main_router
from telecom.core.config import settings

# from telecom.services import create_first_superuser, fill_supp_tables

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main_router)


# @app.on_event('startup')
# async def startup():
#     await create_first_superuser()
#     await fill_supp_tables()
