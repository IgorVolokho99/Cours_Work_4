from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.tools.security import generate_password_digest
from flask_login import current_user

class UsersService(BaseService):
    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_item_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_current_user(self):
        user_id = current_user.get_id()
        if user_id:
            return self.get_item_by_id(user_id)
        else:
            raise ItemNotFound

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create(self, new_pd):
        user_password = new_pd.get("password")
        if user_password:
            new_pd["password"] = generate_password_digest(user_password)
        user = UserDAO(self._db_session).create(new_pd)
        return UserSchema(many=True).dump(user)

    def update(self, new_pd):
        user = UserDAO(self._db_session).update(new_pd)
        return UserSchema().dump(user)


    def update_password(self, new_pd):
        new_pd.get("password_1")
        new_pd.get("password_2")



