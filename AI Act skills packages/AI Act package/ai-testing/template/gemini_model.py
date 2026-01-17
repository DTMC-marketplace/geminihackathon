from deepeval.models import GeminiModel
from deepeval.metrics import AnswerRelevancyMetric
import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

model = GeminiModel(
    model="gemini-3-pro-preview",
    api_key=GEMINI_API_KEY,
    temperature=0,
)
