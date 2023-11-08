from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from schemas.user import RegisterUser
from utils.hashing import Hashing


class UserService:
    def get_all_users(db: Session):
        return db.query(User).all()
    
    def get_user(email: str, db: Session = Depends(get_db)):
        return db.query(User).filter(User.email == email).first()
    
    def create_user(user: RegisterUser, db: Session = Depends(get_db)):
        db_user = User(
            name=user.name,
            email=user.email,
            password=Hashing.bcrypt(user.password),
            is_admin=user.is_admin,
            is_active=user.is_active,
        )
        
        db.add(db_user)
        db.commit()
        
        db.refresh(db_user)
        db_user.password = None
        return db_user
    
    def update_user(user_id: int, user: RegisterUser, db: Session = Depends(get_db)):
        db_user_id = db.query(User).filter(User.id == user_id).first()
        
        db_user_id.name = user.name
        db_user_id.email = user.email
        db_user_id.password = Hashing.bcrypt(user.password)
        db_user_id.is_admin = user.is_admin
        db_user_id.is_active = user.is_active

        db.commit()
        return db_user_id
    
    def deleteUser(user_id: int, db:Session):
        db_user_id = db.query(User).filter(User.id == user_id).first()
        
        db.delete(db_user_id)
        db.commit()
        return db_user_id
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


class UserService2:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_user(self, user: RegisterUser) -> User:
        hashed_password = Hashing.bcrypt(user.password)
        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user_by_email(self, email: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def get_user_by_id(self, id: int) -> User:
        user = self.db.query(User).filter(User.id == id).first()
        return user
    
    # def get_all_users(self) -> list[User]: