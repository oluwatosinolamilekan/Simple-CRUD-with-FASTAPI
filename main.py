from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI,HTTPException

from models import Gender, Role, UpdateUserRequest, User

app = FastAPI()

db: List[User] = [
    User(
            id= uuid4(), 
            first_name = "Jamila",
            last_name = "Ko",
            gender = Gender.female,
            roles = [Role.student]
        ),
    User(
            id= uuid4(), 
            first_name = "Alex",
            last_name = "Ko",
            gender = Gender.male,
            roles = [Role.student,Role.admin]
        )
]

@app.get("/")
def  index():
    return {"Hello": "World"}
  
@app.get("/users")
async  def users():
    return db;

@app.post("/user/create")
async def createUser(user: User):
    db.append(user)
    return {"id": user.id}

@app.put("/user/update/{id}")
async def updateUser(user_update: UpdateUserRequest, id:UUID):
    for user in db:
        if user.id == id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
        raise HTTPException(
            status_code= 404,
            detail=f"user with id: {id} does not exists"
        )

@app.delete("/user/delete/{id}")
async def deleteUser(id: UUID):
     for user in db:
        if user.id == id:
            db.remove(user)
            return
        raise HTTPException(
            status_code= 404,
            detail=f"user with id: {id} does not exists"
        )
