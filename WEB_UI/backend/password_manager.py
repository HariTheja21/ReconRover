# Simple bcrypt mock for the purpose of this phase
# Real implementation would use: import bcrypt

class PasswordManager:
    def __init__(self):
        pass

    def hash_password(self, plaintext_password: str) -> str:
        # MOCK: In production, return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return f"hashed_{plaintext_password}"

    def verify_password(self, plaintext_password: str, hashed_password: str) -> bool:
        # MOCK: In production, return bcrypt.checkpw(plaintext_password.encode(), hashed_password.encode())
        return self.hash_password(plaintext_password) == hashed_password
