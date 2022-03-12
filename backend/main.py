from typing import Optional
from fastapi import FastAPI, HTTPException
from db import connection
import uuid
import hashlib
from fastapi.middleware.cors import CORSMiddleware

from input_types import InputCreateUser
from output_types import OutputUser

app = FastAPI()
origins = [
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/", status_code=201)
async def create_user(request_body: InputCreateUser):
    cur = connection.cursor()
    hash_object = hashlib.sha256(request_body.password.encode('utf-8'))
    cur.execute("INSERT INTO users (id, user_name, password, phone_number,  email) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (str(uuid.uuid4()), request_body.login, hash_object.hexdigest(), request_body.phone_number, request_body.email))
    connection.commit()
    result = cur.fetchone()
    cur.close()
    if result == None:
        raise HTTPException(status_code=500, detail="User cannot create")
    else:
        return {'id': result[0]}


@app.get("/users/{user_id}", response_model=OutputUser)
async def read_user(user_id: str):
    cur = connection.cursor()
    cur.execute(
        "SELECT user_name,phone_number, email FROM users WHERE id = %s;", [user_id])
    result = cur.fetchone()
    cur.close()
    if result == None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return {'id': user_id, 'login': result[0], 'phone_number': result[1], 'email': result[2]}


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    cur = connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", [user_id])
    connection.commit()
    result = cur.fetchone()
    cur.close()
    if result == None:
        raise HTTPException(status_code=500, detail="Cannot delete user")
    else:
        return {'id': result[0]}
