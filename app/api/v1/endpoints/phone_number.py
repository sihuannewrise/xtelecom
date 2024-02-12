from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    tags=["special methods", "xtelecom"],
    summary="Приветствие автора",
    response_description="Описание ответа",
)
def read_root() -> dict[str, str]:
    """
    вместо description - Приветствие пользователя:

    - **name**: имя
    - **surname**: фамилия
    - **age**: возраст (опционально)
    - **is_staff**: является ли пользователь сотрудником
    - **education_level**: уровень образования (опционально)
    """
    return {"hello": "telecom"}
