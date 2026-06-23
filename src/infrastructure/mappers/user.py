from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import HashedPassword
from infrastructure.database.models.user import UserModel


class UserMapper:
    @staticmethod
    def to_entity(row: UserModel) -> User:
        return User(
            user_id=row.id,
            email=Email(row.email),
            hashed_password=HashedPassword(row.hashed_password),
            full_name=row.full_name,
            created_at=row.created_at,
        )

    @staticmethod
    def to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            email=str(user.email),
            hashed_password=str(user.hashed_password),
            full_name=user.full_name,
            created_at=user.created_at,
        )
