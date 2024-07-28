class User:
    def __init__(self, id: int, name: str, email: str, hashed_password: str):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
