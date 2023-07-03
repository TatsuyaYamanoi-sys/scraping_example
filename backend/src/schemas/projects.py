from typing import List, Dict, Union

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime, func

from settings import Base, BaseSession


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text())
    url = Column(String(100))
    reward = Column(Integer)
    on_going = Column(Boolean)
    complieted = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class ProjectManager(BaseSession):
    def __init__(self):
        super().__init__()

    def select_all(self) -> Dict:
        objs = self.__session.query(Project).order_by(Project.id)
        projects = [to_dict(obj) for obj in objs]
        return projects
    
    def select_by_pk(self, pk:int) -> Dict:
        project = self.__session.query(Project).filter_by(id=pk)
        return project

    def select_all_name(self) -> Dict:
        objs = self._session.query(Project.name).order_by(Project.id)
        if objs:
            projects = [to_dict(obj) for obj in objs]
            return projects

    def save(self, obj:Dict):
        try:
            projects = [Project(f'{k}={v}') for k, v in obj.items()]
            self.__session.add_all(projects)
            self.__session.commit()
            self.__session.refresh(projects)
        except:
            self.__session.rollback()

    def update(self, obj:Dict, pk:int):
        try:
            pass
        except:
            self.__session.rollback()
    
    def delete_by_pk(self, pk:int):
        pass