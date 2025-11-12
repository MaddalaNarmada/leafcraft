from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth import create_token

router = APIRouter(prefix="/auth", tags=["authentication"])

# Hardcoded sample user details for authentication
sample_user = {
    "admin@gmail.com": "admin123"
}

#Authenticate user and return a JWT access token.
@router.post("/login", summary="Login to get JWT token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Check user exists (username field will contain email)
    if form_data.username not in sample_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check password (plain text comparison)
    if sample_user[form_data.username] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # generating JWT token
    token = create_token(form_data.username)

    #returning token in the response
    return {"access_token": token, "token_type": "bearer"}
