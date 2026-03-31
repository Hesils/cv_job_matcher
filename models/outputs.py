from typing import Literal

from pydantic import BaseModel

from models.structured import StructuredJob, StructuredCurriculum

class StructureExtractorOutput(BaseModel):
    curriculum: StructuredCurriculum
    job: StructuredJob

class CompatibilityScoreOutput(BaseModel):
    score: int
    justification: str

class Strength(BaseModel):
    element: str
    justification: str

class StrengthOutput(BaseModel):
    strengths: list[Strength]

class Gap(BaseModel):
    element: str
    criticality: Literal["low", "medium", "high"]
    advice: str

class GapOutput(BaseModel):
    gaps: list[Gap]

class KeyWord(BaseModel):
    key_word: str
    context: str

class KeyWordOutput(BaseModel):
    key_words: list[KeyWord]

class Rewording(BaseModel):
    origine: str
    suggested: str
    reason: str

class RewordingOutput(BaseModel):
    rewordings: list[Rewording]