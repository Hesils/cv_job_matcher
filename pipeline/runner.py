from typing import Optional

from pydantic import BaseModel

from agents import (
    RewordingAgent,
    ScoreAgent,
    StrengthsAgent,
    GapsAgent,
    ExtractorAgent,
    KeywordsAgent
)
from agents.base_agent import BaseAgent
from ingestion import JobLoader, CurriculumLoader
from models.inputs import StructureExtractorInput, StandardInput, RewordingAgentInput


class Runner:
    def __init__(self):
        self.job_loader = JobLoader()
        self.curriculum_loader = CurriculumLoader()
        self.output = {}

    def run_job(
            self,
            cv_path: Optional[str] = None,
            cv_content: Optional[str] = None,
            job_content: Optional[str] = None,
            job_url: Optional[str] = None,
    ) -> dict:
        if not cv_path and not cv_content:
            raise ValueError("Must provide either cv_path or cv_content")
        elif not job_content and not job_url:
            raise ValueError("Must provide either job_content or job_url")
        extractor_input = StructureExtractorInput(
            curriculum_content=self.curriculum_loader.load(cv_path, cv_content),
            job_content=self.job_loader.load(job_url, job_content),
        )
        extractor_output = ExtractorAgent().execute(extractor_input, "user")
        agents = [ScoreAgent(), GapsAgent(), KeywordsAgent(), StrengthsAgent(), RewordingAgent()]
        inputs = [
            StandardInput(curriculum=extractor_output.curriculum, job=extractor_output.job)
            for _ in agents[:-1]
        ] + [
            RewordingAgentInput(
                curriculum=extractor_output.curriculum,
                job=extractor_output.job,
                curriculum_content=extractor_input.curriculum_content
            )
        ]
        for agent, query in zip(agents, inputs):
            self.run_agent(agent, query)
        return self.output


    def run_agent(self, agent: BaseAgent, query: BaseModel):
        response = agent.execute(query, "user")
        getattr(self, "output")[agent.name] = response