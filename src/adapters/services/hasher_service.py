import bcrypt

from application.interfaces.hasher_service_port import HasherServicePort

class HasherService(HasherServicePort):
    def hash_password(self, plain: str) -> str:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
