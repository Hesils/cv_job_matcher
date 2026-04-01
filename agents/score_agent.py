from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from models.outputs import CompatibilityScoreOutput
from models.inputs import StandardInput
from prompts.score import SCORE_SYSTEM_PROMPT

class ScoreAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "ScoreAgent",
            model=ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
            ),
            system_prompt=SCORE_SYSTEM_PROMPT,
            output_type=CompatibilityScoreOutput
        )

    def execute(self, request: StandardInput, role: str):
        return super().execute(request.model_dump_json(), role)
