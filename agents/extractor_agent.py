from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from models.outputs import StructureExtractorOutput
from models.inputs import StructureExtractorInput
from prompts.extractor import EXTRACTOR_SYSTEM_PROMPT

class ExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "ExtractorAgent",
            model=ChatOpenAI(
                model="gpt-5-mini",
                temperature=0,
            ),
            system_prompt=EXTRACTOR_SYSTEM_PROMPT,
            output_type=StructureExtractorOutput
        )

    def execute(self, request: StructureExtractorInput, role: str):
        return super().execute(request.model_dump_json(), role)
