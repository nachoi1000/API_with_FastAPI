from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema

router = APIRouter(prefix="/userdb",
                   tags=["userdb"], 
                   responses={status.HTTP_404_NOT_FOUND: {"message":"Not founded"}})



@router.get("/all", response_model= list[User])
async def users():
    return users_schema(db_client.users.find())

# PATH
@router.get("/{id}")
async def get_user(id: str):
    return search_user("_id", ObjectId(id))
# Another form of calling a function inside another.
# QUERY 
@router.get("/")
async def get_user(id: str):
    return search_user("_id", ObjectId(id))
    
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user(field="email", key = user.email)) == User:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User email is already used.")
    
    user_dict = dict(user)
    if "id" in user_dict:
        del user_dict["id"]
    else:
        user_dict["id"] = None

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id":id}))
    return User(**new_user)


@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "The user was not founded."}
   
    return search_user('_id', ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    # Buscar y eliminar el usuario en la base de datos
    result = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user was not found")


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "Not found"}
    
