efrom datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = {secret_key}
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 #Token expiry time set to 1 hour

#oauth2 scheme to extract token from API requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


#create JWT token for given email
def create_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

#validate the JWT token and return user email
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception
