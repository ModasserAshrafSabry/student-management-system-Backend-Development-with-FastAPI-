from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    gpa = Column(Float)

    user_id = Column(Integer, ForeignKey("users.id"))

    # relationship
    user = relationship("User", back_populates="students")
    