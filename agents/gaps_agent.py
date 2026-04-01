from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from models.outputs import GapOutput
from models.inputs import StandardInput
from prompts.gaps import GAPS_SYSTEM_PROMPT

class GapsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "GapsAgent",
            model=ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
            ),
            system_prompt=GAPS_SYSTEM_PROMPT,
            output_type=GapOutput
        )

    def execute(self, request: StandardInput, role: str):
        return super().execute(request.model_dump_json(), role)
