from pydantic import BaseModel

class StructuredCurriculum(BaseModel):
    skills: list[str]
    experiences: list[str]
    educations_and_certifications: list[str]
    years_of_experience: float

class StructuredJob(BaseModel):
    title: str
    required_skills: list[str]
    preferred_skills: list[str]
    context: str
    missions: list[str]

