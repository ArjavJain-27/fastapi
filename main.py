#import necessary libraries
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base,session
from fastapi import FastAPI,Depends

app = FastAPI()

#define the database url and create the engine
database_url = "sqlite:///./test.db"

#create the engine with the database url and set check_same_thread to False
engine = create_engine(database_url,connect_args={"check_same_thread":False})

#set up the sessionmaker with the engine
SessionLocal = sessionmaker (bind=engine)

#create the base class for the declarative model
base = declarative_base()

#define the User model with the necessary columns
class User(base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String,unique=True,index=True)
    password = Column(String)

#create the tables in the database using the base metadata
base.metadata.create_all(bind=engine)    

#define a dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create api endpoint to create a new user in the database
@app.post("/users")
def create_user(user: User, db: session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#read api endpoint to get a all users from the database
@app.get("/users")
def read_users(db: session = Depends(get_db)):
    users = db.query(User).all()
    return users

#read api endpoint to get a user by id from the database
@app.get("/users/{user_id}")
def read_user(user_id: int, db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user

#update api endpoint to update a user by id in the database
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User, db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = updated_user.name
        user.email = updated_user.email
        user.password = updated_user.password
        db.commit()
        db.refresh(user)
    return user 

#delete api endpoint to delete a user by id from the database
@app.delete("/users/{user_id}") 
def delete_user(user_id: int, db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return {"message": "User deleted successfully"}