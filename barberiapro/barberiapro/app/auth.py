from . import models

DEFAULT_ADMIN = ("admin", "admin")

def ensure_default_admin():
    if not models.get_user_by_username(DEFAULT_ADMIN[0]):
        models.create_user(DEFAULT_ADMIN[0], DEFAULT_ADMIN[1])

def verify_user(username, password):
    u = models.get_user_by_username(username)
    if not u:
        return None
    if u["password"] == password:
        return {"id": u["id"], "username": u["username"]}
    return None
