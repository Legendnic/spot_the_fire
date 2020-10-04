from fastapi import FastAPI, Depends, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from services import users_services
from routers import users, satellite_datasets
from Models.pydantic_models import Token
from Models.models import Users
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_services.authenticate_user(Users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=users_services.ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = users_services.create_access_token(
        data = {"sub": user.email, "scopes": form_data.scopes}, expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(users.router)
app.include_router(satellite_datasets.router)
register_tortoise(
    app,
    db_url="mysql://root@localhost:3306/spot_the_fire",
    modules={"models": ["Models.models"]},
    generate_schemas=True
    )