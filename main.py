from typing import Optional
from fastapi import FastAPI, HTTPException
from db import connection
import uuid
import hashlib

from input_types import InputCreateUser

app = FastAPI()

@app.post("/users/", status_code=201)
async def create_user(request_body: InputCreateUser):
    cur = connection.cursor()
    hash_object = hashlib.sha256(request_body.password.encode('utf-8'))
    cur.execute("INSERT INTO users (id, user_name, password, phone_number,  email) VALUES (%s, %s, %s, %s, %s)",
     (str(uuid.uuid4()), request_body.login, hash_object.hexdigest(), request_body.phone_number, request_body.email))
    connection.commit()
    cur.close()
    

@app.get("/users/{user_id}")
def read_user(user_id: str):
    cur = connection.cursor()
    cur.execute("SELECT user_name,phone_number, email FROM users WHERE id = %s;", [user_id])
    result = cur.fetchone()
    cur.close()
    if result == None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return result
    