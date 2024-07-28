import json
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.config import settings


class CRUDUser:
    def _load_users(self) -> List[User]:
        try:
            with open(settings.USERS_FILE_PATH, "r") as file:
                users = json.load(file)
                return [User(**user) for user in users]
        except FileNotFoundError:
            return []

    def _save_users(self, users: List[User]) -> None:
        with open(settings.USERS_FILE_PATH, "w") as file:
            json.dump([user.__dict__ for user in users], file)

    def get_user(self, user_id: int) -> Optional[User]:
        users = self._load_users()
        return next((user for user in users if user.id == user_id), None)

    def get_user_by_email(self, email: str) -> Optional[User]:
        users = self._load_users()
        return next((user for user in users if user.email == email), None)

    def create_user(self, user: UserCreate) -> User:
        users = self._load_users()
        new_id = max([user.id for user in users], default=0) + 1
        hashed_password = user.password + "notreallyhashed"  # Replace with real hashing
        new_user = User(id=new_id, name=user.name, email=user.email, hashed_password=hashed_password)
        users.append(new_user)
        self._save_users(users)
        return new_user


crud_user = CRUDUser()
