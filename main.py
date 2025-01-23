"""
project/
│
├── app/
│   ├── __init__.py           # Marks the directory as a Python package
│   ├── crud.py               # CRUD operations
│   ├── models.py             # SQLAlchemy models
│   └── schema.py             # Pydantic models (UserUpdate, UserResponse, etc.)
│
├── main.txt                  # FastAPI application entry point
└── requirements.py           # Python dependencies


"""
# uvicorn main:app --reload
# uvicorn main:app --host 127.0.0.1 ---port 8080 --workers 4 --log-level debug
# fastapi dev main.py
# python main.py
from types import NoneType
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn

from app import schema, crud, models
from app.database import get_db
from app.models import User
from app.schema import UserCreate, UserUpdate, UserResponse


# app = FastAPI(
#     title="FastAPI CRUD",
#     description="Fast API CRUD operations",
#     summary="basic crud operations",
#     version="0.0.1",
#     contact={
#         "name": "FAST USER",
#         "email": "fastuser@email.com",
#     },
# )

app = FastAPI()

@app.get('/')
def hello_world():
    data = {"message": "Hello from FastAPI"}
    return JSONResponse(content=data, status_code=200)

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}


@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session =Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.put("/user/{user_id}",response_model = schema.UserUpdate)
def put_user(user_id: int, user_update: schema.UserUpdate, db: Session = Depends(get_db)):
    if not user_update.name or not user_update.email or not user_update.age:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields are required to update the user."
        )

    db_user = crud.update_user(db, user_id, user_update)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@app.patch("/user/{user_id}", response_model=schema.UserUpdate)  # Ensure the response model is Pydantic
def patch_user(user_id: int, user_patch: schema.UserPatch, db: Session = Depends(get_db)):
    db_user = crud.patch_user(db, user_id, user_patch)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user  # db_item will be converted to a Pydantic model automatically due to orm_mode

@app.delete("/user/{user_id}")
def delete_user_by_email(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)



