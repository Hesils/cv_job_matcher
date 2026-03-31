from pydantic import BaseModel

from models.structured import StructuredCurriculum, StructuredJob

class AgentInput(BaseModel):
    messages: list[dict]

class StructureExtractorInput(BaseModel):
    curriculum_content: str
    job_content: str

class StandardInput(BaseModel):
    curriculum: StructuredCurriculum
    job: StructuredJob

class RewordingAgentInput(BaseModel):
    curriculum: StructuredCurriculum
    job: StructuredJob
    curriculum_content: str