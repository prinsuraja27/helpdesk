from pydantic import BaseModel, Field


class StudentRequest(BaseModel):
    request_id: str = Field(..., min_length=1)
    student_name: str = Field(..., min_length=1)
    enrollment: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    phone: str
    email: str = Field(..., min_length=1)
    request_type: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class RequestStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|progress|solved|rejected)$")
