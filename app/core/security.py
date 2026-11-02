import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from app.db.database import get_db
from app.models.user import users


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

ALGORITHM = 'HS256'

ACCESS_TOKEN_EXPIRE_LIMIT = 30


def hash_password(password):
    pwd_bytes = password.encode("utf-8")
    gensalt = bcrypt.gensalt()
    hash = bcrypt.hashpw(pwd_bytes, salt=gensalt)
    return hash.decode("utf-8")

def verify_password (plain, hashed):
    plain_bytes = plain.encode("utf-8")
    hash_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_bytes,hash_bytes)

def jwt_create (data : dict, expire_time : timedelta|None=None):
    to_encode = data.copy()
    if expire_time:
        expire = datetime.utcnow + expire_time
    else: 
        expire = (datetime.utcnow()) + (timedelta(minutes=15))
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth = OAuth2PasswordBearer(tokenUrl="/users/login")

def jwt_auth (token : str = Depends(oauth), db:session = Depends(get_db)):
    exception = HTTPException(status_code=401 , detail="unauthorized access")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str =  payload.get('sub')
        if email is None:
            raise exception
    except:
        raise exception

    user = db.query(users).filter(email == users.email).first()
    if user is None:
        raise exception
    
    return user