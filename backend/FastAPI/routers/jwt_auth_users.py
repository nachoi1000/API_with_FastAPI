from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "4e5e6f7b8c6a1a9b5e4b3d8e2f5a6b7c4d1e9f7a6b5c4d3e5f2a6d4c9b7e2a6"

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disables: bool

class UserDB(User):
    password: str


users_db = {
    "gatitosdev":{
        "username": "gatitosdev",
        "full_name": "Brais Moure",
        "email": "tinelli@gmail.com",
        "disables": False,
        "password": "$2a$12$tdEOpTy2XM6ntSnOgQeJN.O6.aTDqInKt/ciJkWcuVxG5z99javGi"
    },
    "gatitosdev2":{
        "username": "gatitosdev2",
        "full_name": "Brais Moure2",
        "email": "tinelli2@gmail.com",
        "disables": True,
        "password": "$2a$12$gvZNqIPLz/56NS1TXtRDlejtmFmLP54mOQJV6ufsVno57w6rteGfK"
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Invalid Auth Credentials",
                                headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token=token, key=SECRET, algorithms=ALGORITHM).get("user")
        if username is None:
            raise exception

    except JWTError:
            raise exception
        
    return search_user(username=username)
    

async def current_user(user: User = Depends(auth_user)):        
    if user.disables:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Inactive user")
    
    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not correct")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not correct")

    access_token = {"user": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
                    }
    
    return {"access_token": jwt.encode(access_token, SECRET, ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user