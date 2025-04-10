from uuid import uuid4

fake_users_db = {}
fake_users_db["admin@example.com"].role = "admin"

class User:
    def __init__(self, email: str, hashed_password: str, role: str = "user"):
        self.id = str(uuid4())
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
