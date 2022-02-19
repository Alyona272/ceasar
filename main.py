from fastapi import FastAPI, HTTPException
from db import connection
import uuid
import hashlib
import requests
from in_memory_storage import InMemoryStorage

from input_types import InputCreateUser
from output_types import OutputUser

app = FastAPI()
storage = InMemoryStorage()

@app.post("/users/", status_code=201)
async def create_user(request_body: InputCreateUser):
    try:
        user_id = str(uuid.uuid4())
        storage.save_user(request_body, user_id)
        return {'id': user_id}
    except:
        raise HTTPException(status_code=500, detail="User cannot create")


@app.get("/users/{user_id}", response_model=OutputUser)
async def read_user(user_id: str):
    try:
        result = storage.get_user(user_id)
        return result
    except:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        storage.delete_user(user_id)
        return {'id': user_id}
    except:
        raise HTTPException(status_code=500, detail="Cannot delete user")

@app.get("/cities/names")
async def get_cities_names():
    r = requests.get('https://kudago.com/public-api/v1.4/locations/?lang=&fields=&order_by=')
    names = [city['name'] for city in r.json()]
    return names