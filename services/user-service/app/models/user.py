from uuid import uuid4

fake_users_db = {}
fake_tenants_db = {}

class User:
    def __init__(self, email: str, hashed_password: str, tenant: str, role: str = "user"):
        self.id = str(uuid4())
        self.email = email
        self.hashed_password = hashed_password
        self.tenant = tenant
        self.role = role
