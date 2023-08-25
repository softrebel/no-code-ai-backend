from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from .settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_url = settings.TOKEN_URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)
