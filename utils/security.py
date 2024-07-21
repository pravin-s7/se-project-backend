from fastapi import HTTPException, Depends, status, Security, APIRouter, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from models.model import User, Token, TokenData
from fastapi.security import HTTPBearer, SecurityScopes
from fastapi.responses import RedirectResponse
from typing import Annotated
from pydantic import ValidationError
import jwt
import requests
from jwt.exceptions import InvalidTokenError
from utils.validation import UserNotFound
from database.db import db
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

auth = APIRouter(tags=['Auth'])

# defining oauth_scheme
bearer_auth = HTTPBearer(scheme_name="BearerAuth", auto_error=False)

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

GOOGLE_CLIENT_ID =  os.environ.get('GOOGLE_CLIENT_ID')  
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI =  os.environ.get('GOOGLE_REDIRECT_URI')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(email: str):
    user = db.user.find_one({"email": email})
    if user:
        return User(**user)
    else:
        raise UserNotFound(error_code="User_404", error_message="User not found in the database")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt    


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(bearer_auth)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        if not token:
            raise credentials_exception
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, email=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@auth.get("/login/google")
async def login_google():
    redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    return redirect_url


@auth.get('/oauth/callback')
def oauth_callback(request: Request):
    # Extract query parameters from the request
    code = request.query_params.get('code')
    scope = request.query_params.get('scope')

    # Handle the Authentication and token exchange
    id_token, user_info = exchange_code_for_id_token(code, scope)
    print(user_info.json())

    # Decode the ID token to extract user information
    decoded_token = decode_jwt_token(id_token)
    
    # Access user specific claims
    user_id = decoded_token.get('sub')
    user_email = decoded_token.get('email')
    email_verified = decoded_token.get('email_verified')
    
    # Validate and process user authentication
    if email_verified:
        access_token = handle_authenticated_user(user_email, user_info.json())
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(status_code=401, detail="User not verified")

def exchange_code_for_id_token(code, scope):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": scope,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    response_data = response.json()
    id_token = response_data.get("id_token")
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return id_token, user_info

def decode_jwt_token(id_token):
    return jwt.decode(id_token, options={"verify_signature": False})

def handle_authenticated_user(user_email, user_info):
    try:
        user = get_user(email=user_email)
    except UserNotFound:
        create_new_user(user_info)
        user = get_user(email=user_email)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "scopes": user.roles},
        expires_delta=access_token_expires
    )
    return access_token

def create_new_user(user_info):
    db.user.insert_one({
        "name": user_info.get('name'),
        "email": user_info.get('email'),
        "roles": ["user"],
        "disabled": False
    })


