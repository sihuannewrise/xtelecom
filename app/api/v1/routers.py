from fastapi import APIRouter

from app.api.v1.endpoints.phone_number import router as phone_number_router

main_router = APIRouter()
main_router.include_router(
    phone_number_router,
    prefix='/phone_numbers',
    tags=['Phone numbers']
)
