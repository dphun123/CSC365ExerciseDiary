from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import os
from supabase import create_client, Client
import re

router = APIRouter(
  prefix="/user",
  tags=["user"],
)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class Credentials(BaseModel):
  email: str
  password: str

email_regex = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

password_regex = re.compile(
    r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*[a-zA-Z]).{8,}$'
)

authorize = OAuth2PasswordBearer(tokenUrl="user/login")

@router.post("/signup")
def sign_up(credentials: Credentials):
  if not email_regex.match(credentials.email):
    raise HTTPException(status_code=400, detail="Invalid email.")
  if not password_regex.match(credentials.password):
    raise HTTPException(status_code=400, detail="Password must be at least 8 characters, contain one uppercase letter, and contain one special character.")
  try:
    supabase.auth.sign_up({
      "email": credentials.email,
      "password": credentials.password,
    })
    return "You have successfully been signed up!"
  except Exception as e:
    if str(e) == 'User already registered':
      raise HTTPException(status_code=409, detail="User already registered! Login.")
    raise HTTPException(status_code=500, detail="Something went wrong!")
  
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  """Have to login through the lock. Use email for username."""
  try:
    res = supabase.auth.sign_in_with_password({
      "email": form_data.username,
      "password": form_data.password,
    })
    return {"message": "Login success. (note: you have to login through the lock)",
            "user": res.user}
  except Exception as e:
    if str(e) == 'Invalid login credentials':
      raise HTTPException(status_code=401, detail="Invalid login credentials. Try again.")
    raise HTTPException(status_code=500, detail="Something went wrong!")
  
def get_user():
  res = supabase.auth.get_session()
  return res.user.email