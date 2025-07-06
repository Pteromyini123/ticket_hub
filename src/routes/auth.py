from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
import httpx

router = APIRouter()

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

DUMMY_LOGIN_URL = "https://dummyjson.com/auth/login"

class LoginData(BaseModel):
    username: str
    password: str


# test auth info:
# {
#   "username": "emilys",
#   "password": "emilyspass"
# }


@router.post("/login")
async def login(data: LoginData):
    async with httpx.AsyncClient() as client:
        response = await client.post(DUMMY_LOGIN_URL, json=data.dict())

        print("Status:", response.status_code)
        print("Response:", response.text)

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = response.json()
        token = jwt.encode({"sub": user["username"]}, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": token, "token_type": "bearer"}



from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError


security = HTTPBearer()

#enter only the token in the field "Authorise", not "Bearer <token>"
# check the token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print("TOKEN RECEIVED:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
