from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


SECRET_KEY = "tPgqIXCzZVP3eRVyXeKUKzdsrTBJjT" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


# This is to verify the password passing in a function plain
# and hashed and using the method ".verify" then passing the arguments
def validate_user(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt