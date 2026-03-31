from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from models.outputs import StrengthOutput
from models.inputs import StandardInput
from prompts.strengths import STRENGTHS_SYSTEM_PROMPT

class StrengthsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "StrengthsAgent",
            model=ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
            ),
            system_prompt=STRENGTHS_SYSTEM_PROMPT,
            output_type=StrengthOutput
        )

    def execute(self, request: StandardInput, role: str):
        super().execute(request.model_dump_json(), role)
