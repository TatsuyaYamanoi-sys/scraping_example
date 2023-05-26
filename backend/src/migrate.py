from schemas import User
from settings import Base, BaseEngine


class Migration(object):
    def __init__(self):
        self.e = BaseEngine().engine

    def create_all(self):
        Base.metadata.create_all(self.e)


if __name__ == '__main__':
    Migration().create_all()