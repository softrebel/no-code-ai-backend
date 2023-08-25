from typing import Union
from fastapi import FastAPI, Depends, Request

import os
from dotenv import load_dotenv
from pathlib import Path
from api.v1 import auth_endpoints, file_endpoints, model_endpoints

from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from fastapi.exceptions import HTTPException
from utils.handle_exceptions import exception_handlers
from configs.database import init


app = FastAPI(exception_handlers=exception_handlers)
# app=FastAPI()
# v1
app.include_router(auth_endpoints.router, prefix="/v1")
app.include_router(file_endpoints.router, prefix="/v1")
app.include_router(model_endpoints.router, prefix="/v1")


@app.on_event("startup")
async def startup_event():
    await init()


@app.get('/')
def root(request: Request):
    clientIp = request.client.host
    return {"Hello": "World", "ip": clientIp}
