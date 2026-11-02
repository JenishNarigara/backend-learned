from app.db.database import get_db
from app.models.user import users
from app.schemas.user import usercreate, userresponse, userlogin, userprofile
from app.core.security import hash_password, verify_password, jwt_create, jwt_auth
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import session
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix='/users', tags=['users'])

@router.post('/create')
def create_user(user: usercreate, db : session = Depends(get_db)):
    db_query = db.query(users).filter(user.email == users.email).first()
    if db_query:
        raise HTTPException(status_code=400 , detail="email already exists")
    else :
        hashed = hash_password(password=user.password)
        user_add = users(email=user.email, password=hashed)
        db.add(user_add)
        db.commit()
        db.refresh(user_add)
        return{"password" : hashed}


@router.post('/login')
def login_user(user : OAuth2PasswordRequestForm = Depends(), db : session = Depends(get_db)):
    db_query = db.query(users).filter(user.username == users.email).first()
    if db_query:
        check = verify_password(user.password, db_query.password)
        if check:
            return { "access_token": jwt_create(data={"sub" : user.username}), "token_type" : "bearer"}
        else:
            raise HTTPException(status_code=400, detail="email or password is invalid")
    
    else : 
        raise HTTPException(status_code=400, detail="email or password is incorrect")

@router.get('/profile')
def get_profile(user : users = Depends(jwt_auth)):
    return{
        "message" : "secure login",
        "email" : user.email
    }