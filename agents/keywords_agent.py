from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from models.outputs import KeyWordOutput
from models.inputs import StandardInput
from prompts.keywords import KEYWORDS_SYSTEM_PROMPT

class KeywordsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "KeywordsAgent",
            model=ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
            ),
            system_prompt=KEYWORDS_SYSTEM_PROMPT,
            output_type=KeyWordOutput
        )

    def execute(self, request: StandardInput, role: str):
        return super().execute(request.model_dump_json(), role)
