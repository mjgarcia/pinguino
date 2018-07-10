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

connectionString = 'mysql://{}:{}@localhost/pinguino'.format(secrets.mysqlUsername, secrets.mysqlPassword)
engine = create_engine(connectionString)

Base.metadata.create_all(engine)