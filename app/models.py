from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from app.database import Base
from datetime import datetime, timezone


class Course(Base):
    __tablename__ = "course"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    author = Column(String(255), index=True, nullable=False)
    duration = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    discount = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}')>"
    
class Video(Base):
    __tablename__ = 'video'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author = Column(String(100))
    file_path = Column(String(255), nullable=False)  # Path to the MP3 on disk
