from deepteam import red_team
from deepteam.vulnerabilities import Bias
from deepteam.attacks.single_turn import PromptInjection

from deepeval.models import GeminiModel
import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

model = GeminiModel(
    model="gemini-2.5-flash",
    api_key=GEMINI_API_KEY,
    temperature=0,
)

async def model_callback(input: str, turns=None):
    # Call your LLM app here
    return f"I'm sorry, but I can't answer {input}"


bias = Bias(types=["race"])
prompt_injection = PromptInjection()

red_team(
    model_callback=model_callback,
    vulnerabilities=[bias],
    attacks=[prompt_injection],
    simulator_model=model, evaluation_model=model
)