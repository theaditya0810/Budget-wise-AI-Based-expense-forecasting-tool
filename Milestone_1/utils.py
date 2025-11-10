import jwt
import datetime
import bcrypt

SECRET_KEY = "budgetwise_secret_key"

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_jwt_token(email):
    payload = {"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
