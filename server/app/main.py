from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)

SECRET_KEY =  os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRE = int(os.getenv('TOKEN_EXPIRE'))

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

app = FastAPI()

from server.app.router.auth import auth_router
from server.app.router.order import order_router
app.include_router(auth_router)
app.include_router(order_router)