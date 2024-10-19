# models.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rule_string = Column(String)

# Database setup function
def init_db():
    engine = create_engine('sqlite:///rules.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

