from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from models.outputs import RewordingOutput
from models.inputs import RewordingAgentInput
from prompts.rewording import REFORMULATIONS_SYSTEM_PROMPT

class RewordingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "RewordingAgent",
            model=ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
            ),
            system_prompt=REFORMULATIONS_SYSTEM_PROMPT,
            output_type=RewordingOutput
        )

    def execute(self, request: RewordingAgentInput, role: str):
        return super().execute(request.model_dump_json(), role)
