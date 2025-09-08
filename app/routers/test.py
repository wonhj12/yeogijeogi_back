from fastapi import APIRouter

from app.db.models.users import Users


router = APIRouter()

router = APIRouter(
    prefix="/test",
    tags=["test"],
)


@router.get("/")
def read_root():
    return {"Test": "Test"}


@router.post(
    "/create-user",
    status_code=201,
    responses={
        401: {"description": "Invalid Token"},
        500: {"description": "Internal Server Error"},
    },
)
async def test_create_user():
    import uuid

    user_id = str(uuid.uuid4())
    new_user = Users(id=user_id)

    await new_user.create()

    return True
