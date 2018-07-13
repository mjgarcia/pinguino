from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import secrets

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    task = Column(Integer, nullable=False)

connection_string = 'mysql://{}:{}@localhost/pinguino'.format(secrets.mysql_username, secrets.mysql_password)
engine = create_engine(connection_string)

Base.metadata.create_all(engine)