from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    name: str
    department: str
    gpa: float = Field(..., ge=0, le=4)  # 👈 validation

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
        

        