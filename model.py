from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

root = Path.cwd()
engine = create_engine(f'sqlite:///{root}/weixin_friends.sqlite')
Session = sessionmaker(engine)

Base = declarative_base()


class Friend(Base):
    __tablename__ = 'friend'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nick_name = Column(String)
    remark_name = Column(String)
    call_name = Column(String)
    already_send = Column(Boolean)

    def __repr__(self):
        return f'<Friend {self.remark_name}>'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
