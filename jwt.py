from fastapi import FastAPI,HTTPException,Depends,Header
from jose import jwt
from datetime import datetime, timedelta,timezone

app = FastAPI()

SECRET_KEY = "your_secret_key"

ALGORITHM = "HS256"

#create the access token
def create_access_token(data: dict, expire: timedelta = None):
    to_encode = data.copy()
    if expire is not None:
        expire_time = datetime.now(timezone.utc) + expire
        to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#login api endpoint
@app.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "password":
        raise HTTPException(status_code=200, detail={"access_token": create_access_token({"sub": username}), "token_type": "bearer"})
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

#token verification dependency
def verify_token(authorization: str = Header(...)):
    try:
        payload = jwt.decode(authorization.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")    

#protected api endpoint
@app.get("/protected")
def protected_route(user = Depends(verify_token)):
    return {"message": "This is a protected route", "user": user["sub"]}    