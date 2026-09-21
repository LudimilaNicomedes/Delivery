from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from server.app.models import db, User
from server.app.main import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError

def catch_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def check_token(token: str = Depends(oauth2_schema), session: Session = Depends(catch_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user  = int(dic_info.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401, detail='Access denied')
    
    user = session.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid access')
    return user