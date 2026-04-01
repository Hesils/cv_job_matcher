from concurrent.futures import ThreadPoolExecutor, as_completed
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
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self._run_agent_safe, agent, query)
                for agent, query in zip(agents, inputs)
            ]

            for future in as_completed(futures):
                name, result = future.result()
                self.output[name] = result

        return self.output

    @staticmethod
    def _run_agent_safe(agent: BaseAgent, query: BaseModel):
        response = agent.execute(query, "user")
        return agent.name, response
