from storage import UserStorage
from input_types import InputCreateUser


class InMemoryStorage(UserStorage):

    def __init__(self):
        self.data = {}

    def save_user(self, user: InputCreateUser, id: str):
        self.data[id] = user
        return True

    def delete_user(self, id: str):
        del self.data[id]
        return True

    def get_user(self, id: str):
        result = self.data[id]
        return {'id': id, 'login': result['login'], 'phone_number': result['phone_number'], 'email': result['email']}


        