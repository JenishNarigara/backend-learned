from pydantic import BaseModel, EmailStr

class usercreate(BaseModel):
    email : EmailStr
    password : str

class userresponse(BaseModel):
    id : int
    password : str

class userlogin(BaseModel):
    email : EmailStr
    password : str

class userprofile(BaseModel):
    token : str