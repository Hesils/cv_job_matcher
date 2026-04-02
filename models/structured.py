from pydantic import BaseModel

class PersonalProject(BaseModel):
    title: str
    description: str
    technologies: list[str]
    key_decisions: list[str]

class StructuredCurriculum(BaseModel):
    skills: list[str]
    experiences: list[str]
    educations_and_certifications: list[str]
    years_of_experience: float
    personal_projects: list[PersonalProject]

class StructuredJob(BaseModel):
    title: str
    required_skills: list[str]
    preferred_skills: list[str]
    context: str
    missions: list[str]
    min_years_required: float

