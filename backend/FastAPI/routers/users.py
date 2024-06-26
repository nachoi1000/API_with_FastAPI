from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# USER CLASS
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_lists = [User(id=1, name="Tito", surname="Ramirez", url="http://golessonamores.com", age=45),
               User(id=2, name="Matias", surname="Hais", url="http://hanson.net", age=55),
               User(id=3, name="Javiera", surname="Chilena", url="http://mamasita.com", age=30),]

@router.get("/users")
async def create_users():
    return users_lists

# PATH
@router.get("/user/{id}")
async def get_user(id: int):
    return search_user(id)


# Another form of calling a function inside another.
# QUERY 
@router.get("/user/")
async def get_user(id: int):
    return search_user(id)
    
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if search_user(user.id):
        raise HTTPException(status_code=404, detail="User already exist")
    else:
        users_lists.append(user)
        return user

@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_lists):
        if saved_user.id == user.id:
            users_lists[index] = user
            found = True

    if not found:
        return {"error": "The user was not founded."}
    else:
        return user


@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_lists):
        if saved_user.id == id:
            del users_lists[index]
            found = True
            return saved_user
        
    if not found:
        return {"error": "The user was not founded."}


def search_user(id: int):
    users = filter(lambda x: x.id == id, users_lists)
    try:
        return list(users)
    except:
        return ""


