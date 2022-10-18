from sqlalchemy import PrimaryKeyConstraint, create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('sqlite:///iot.db', echo=True)
Base = declarative_base()

# for creating a session

Session = sessionmaker(bind=engine, autoflush=True)


# Model Table Classes

class JsonModel(object):
    def _tojson(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class PinTable(Base,JsonModel):
    __tablename__ = 'pin_table'
    pin = Column(Integer, primary_key = True)
    current_status = Column(Integer)
    last_update = Column(DateTime)

