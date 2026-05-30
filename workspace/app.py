class UserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, user_id: str, email: str) -> dict:
        if user_id in self.users:
            raise ValueError("User already exists")
        
        user_profile = {"id": user_id, "email": email, "tier": "free"}
        self.users[user_id] = user_profile
        return user_profile

    def get_user(self, user_id: str) -> dict:
        return self.users.get(user_id, {})

    def upgrade_to_premium(self, user_id: str) -> dict:
        if user_id not in self.users:
            raise KeyError(f"User with ID '{user_id}' not found.")
        
        user_profile = self.users[user_id]
        user_profile["tier"] = "premium"
        return user_profile