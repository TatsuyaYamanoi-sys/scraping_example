from typing import List, Dict, Union

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func

from settings import Base, BaseSession


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    email = Column(String(20), unique=True, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class UserManager(BaseSession):
    def __init__(self):
        super().__init__()

    def select_all(self) -> Dict:
        objs = self.__session.query(User).order_by(User.id)
        users = [to_dict(obj) for obj in objs]
        return users
    
    def select_by_pk(self, pk:int) -> Dict:
        user = self.__session.query(User).filter(id=pk)
        return user

    def save(self, obj:Dict):
        try:
            user = obj
            self.__session.add(user)
            self.__session.commit()
            self.__session.refresh(user)
        except:
            self.__session.rollback()

    def update(self, obj:Dict, pk:int):
        try:
            pass
        except:
            self.__session.rollback()
    
    def delete_by_pk(self, pk:int):
        pass