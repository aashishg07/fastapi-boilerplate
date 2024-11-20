from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


# This is to verify the password passing in a function plain
# and hashed and using the method ".verify" then passing the arguments
def validate_user(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)