from storage import UserStorage
from input_types import InputCreateUser
from db import connection

class PgStorage(UserStorage):

    def __init__(self):
        self.connection = connection
        

    def save_user(self, user: InputCreateUser, id: str):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO users (id, user_name, password, phone_number,  email) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (id, user.login, user.password, user.phone_number, user.email))
        self.connection.commit()
        result = cur.fetchone()
        cur.close()
        if result == None:
            raise 
        else:
            return {'id': result[0]}

    def delete_user(self, id: str):
        cur = self.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", [id])
        connection.commit()
        result = cur.fetchone()
        cur.close()
        if result == None:
            raise 
        else:
            return {'id': result[0]}

    def get_user(self, id: str):
        cur = connection.cursor()
        cur.execute(
            "SELECT user_name,phone_number, email FROM users WHERE id = %s;", [id])
        result = cur.fetchone()
        cur.close()
        if result == None:
            raise 
        else:
            return {'id': id, 'login': result[0], 'phone_number': result[1], 'email': result[2]}
