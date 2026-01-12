from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class VMResource(Base):
    __tablename__ = "vm_resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    resource_group = Column(String)
    location = Column(String)
    status = Column(String)
    size = Column(String, nullable=True)
    fetched_at = Column(DateTime, default=datetime.now())

# Database URL from environment (from docker-compose)
DATABASE_URL = "postgresql://postgres:devsecret@db:5432/cloudmonitor"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)