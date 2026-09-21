from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from server.app.schemas import UserSchema, LoginSchema
from server.app.dependencies import catch_session, check_token
from server.app.models import User
from sqlalchemy.orm import Session
from server.app.main import bcrypt_context, SECRET_KEY, ALGORITHM, TOKEN_EXPIRE
from sqlalchemy import or_
from jose import jwt
from datetime import datetime, timezone, timedelta

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

def create_token(id_user, duration_token = timedelta(minutes= TOKEN_EXPIRE )):
    date_expiration = datetime.now(timezone.utc) + duration_token
    dic_inf= {'sub': str(id_user), 'exp': date_expiration}
    encode_jwt = jwt.encode(dic_inf, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email ==email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

@auth_router.post('/')
async def home():
    '''
    This is the systems default authentication route 
    '''
    return {'authenticated':  False}

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(catch_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="invalid email or password")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration_token=timedelta(days=20))
        return {
            'acess_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }
#Só para fazer o botão de Authorize da documentação funcionar 
@auth_router.post('/login-form')
async def login_form(form_data: OAuth2PasswordRequestForm =  Depends(), session: Session = Depends(catch_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="invalid email or password")
    else:
        access_token = create_token(user.id)
        return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }

@auth_router.get('/refresh')
async def use_refresh_token(user: User = Depends(check_token)):
    access_token = create_token(user.id)
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }

@auth_router.post('/create')
async def create_account(user_schema: UserSchema, session: Session = Depends(catch_session)):
    user = session.query(User).filter(or_(User.email ==  user_schema.email, User.phone == user_schema.phone)).first()

    if user:
        if user.email == user_schema.email:
            raise HTTPException(status_code=400, detail="email already registered")
        if user.phone == user_schema.phone:
            raise HTTPException(status_code=400, detail="phone already registered")
    else:
        password_encrypted = bcrypt_context.hash(user_schema.password)
        new_account = User(user_schema.name, user_schema.email, user_schema.phone, password_encrypted, user_schema.asset, user_schema.admin)
        session.add(new_account)
        session.commit()
        return {'message': f'User successfully registered {user_schema.email}'}

