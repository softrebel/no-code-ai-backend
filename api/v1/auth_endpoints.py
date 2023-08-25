from datetime import timedelta
from typing_extensions import Annotated
from fastapi import APIRouter
from schemas.user import UserView, User, UserCreating
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from services.auth_service import AuthService
from utils.hashing import (verify_password,
                           create_access_token,
                           get_password_hash)
from configs.authentication import oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.response import Response
from jose import jwt, JWTError
from schemas.token import TokenData
router = APIRouter()


async def authenticate_user(username: str, password: str) -> UserView:
    service = AuthService()
    user = await service.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    output = UserView(id=user.id,
                      username=user.username,
                      disabled=user.disabled,
                      fullname=user.fullname)
    return output


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    service = AuthService()
    user = await service.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    # output = UserView(id=current_user.id,
    #                        username=current_user.username,
    #                        disabled=current_user.disabled,
    #                        fullname=current_user.fullname)
    return current_user


@router.post('/auth')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me")
async def read_users_me(current_user: Annotated[
    User, Depends(get_current_active_user)
]) -> UserView:
    return current_user


@router.post('/auth/register')
async def register_user(
    user: UserCreating
):
    if user.password != user.repeat_password:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        message='passwords doesnt match',
                        data={})
    exists = await User.find_one(User.username == user.username)
    if exists:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        message='username exists',
                        data={})
    hashed_password = get_password_hash(user.password)
    item = User(fullname=user.fullname, username=user.username,
                hashed_password=hashed_password, disabled=user.disabled)
    await item.create()

    return Response(status=status.HTTP_200_OK,
                    message='successfully created',
                    data={'_id': str(item.id), 'username': item.username})
