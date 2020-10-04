from Models.pydantic_models import User_Pydantic, UserIn_Pydantic
from Models.models import Users
from fastapi import APIRouter, Depends, Security
from services.users_services import get_password_hash, get_current_user

router = APIRouter()

@router.post('/users/', response_model=User_Pydantic, tags=['users'])
async def create_user(user: UserIn_Pydantic):

    user.password = get_password_hash(user.password)

    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.get("/users/me/", response_model=User_Pydantic, tags=['users'])
async def read_users_me(current_user: User_Pydantic = Security(get_current_user, scopes=["me"])):
    return current_user