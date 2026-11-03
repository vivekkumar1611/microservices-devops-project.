
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="User Service", version="1.1.0")

users: dict[int, dict] = {}
next_id = 1


class UserIn(BaseModel):
    name: str
    email: EmailStr


@app.get("/")
def root():
    return {"service": "user-service", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}


@app.get("/users")
def list_users():
    return list(users.values())


@app.post("/users", status_code=201)
def create_user(user: UserIn):
    global next_id

    for existing_user in users.values():
        if existing_user["email"].lower() == str(user.email).lower():
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

    record = {
        "id": next_id,
        **user.model_dump()
    }

    users[next_id] = record
    next_id += 1

    return record


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return users[user_id]


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = users.pop(user_id)

    return {
        "message": "User deleted successfully",
        "user": deleted_user
    }
