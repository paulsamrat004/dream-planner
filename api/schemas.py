from pydantic import BaseModel, Field, field_validator

class PlanRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=60)
    city: str = Field(min_length=1)
    education: str = Field(min_length=1)
    job_role: str = Field(min_length=1)
    monthly_salary: float = Field(gt=0)
    marriage_years: int = Field(ge=1, le=50)
    car_years: int = Field(ge=1, le=50)
    home_years: int = Field(ge=1, le=50)
    saving_percent: float = Field(ge=0, le=100)
    area_type: str | None = None

    @field_validator("city", "education", "job_role")
    @classmethod
    def not_blank(cls, v):
        if not v.strip():
            raise ValueError("Value cannot be blank.")
        return v.strip()

class AgentRequest(BaseModel):
    message: str = Field(min_length=10, max_length=2000)

class RAGQuestion(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
