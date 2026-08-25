from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta,timezone
from jose import jwt
from passlib.context import CryptContext

app = FastAPI()

#jwt configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"])

#oauth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#dummby user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("password")
    }
}

#hash password
def hash_password(password: str):
    return pwd_context.hash(password)

#verify password
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


#create the access token
def create_access_token(data: dict, expire: timedelta = None):
    to_encode = data.copy()
    if expire is not None:
        expire_time = datetime.now(timezone.utc) + expire
        to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#login api (OAuth2PasswordRequestForm) endpoint
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": create_access_token({"sub": form_data.username}), "token_type": "bearer"}

#token verification dependency
def verify_token(authorization: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(authorization.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")    

#protected api endpoint
@app.get("/protected")
def protected_route(user = Depends(verify_token)):
    return {"message": "This is a protected route", "user": user["sub"]}    