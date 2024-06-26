from typing import Union

from fastapi import FastAPI
import uvicorn
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Routers
# Si hay mas de una ruta que se repite: @router.post("/login") @router.get("/users/me") como identifico el de que router se ejecuta? del que esta definido primero?: Se ejecuta la ultima definida.
app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return "Hola Gatossss"


@app.get("/url")
async def url():
    return {"url_2":"kajkajdsjksa"}


#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)

# swagger documentation: GET /docs

#step1: go to the root where main.py is. C:\Users\nacho\OneDrive\Desktop\Backend_with_FastAPI\backend\FastAPI
#Step2: initialize server-> command: uvicorn main:app --reload 



#Url="https://www.youtube.com/watch?v=_y9qQZXE24A&t=3374s"
#min="7.35.00" 

# Authentication: It means that the system knows/identifies the user who has get in. Make a login
# Authorization: it meas that the user has permissons to enter toi specific part of the system.

#DUDA:
# Por que la base de datos se llama users, si el .py del schema se llama user?