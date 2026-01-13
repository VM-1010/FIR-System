from werkzeug.security import check_password_hash, generate_password_hash
import database 
from enum import IntEnum

class Lstatus(IntEnum):
    success = 0,
    user_not_registered = 1,
    wrong_password = 2,
    server_issue = 3

def check_login(username: str, password: str) -> Lstatus:
    pwd = database.get_password(username)
    if not pwd:
        return Lstatus.user_not_registered
    if not check_password_hash(pwd, password):
        return Lstatus.wrong_password
    
    
        