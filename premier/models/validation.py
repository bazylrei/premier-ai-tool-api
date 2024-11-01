from pydantic import BaseModel
from typing import List

class Validation(BaseModel):
    confidence_percentage: int
    reasons_for_relevance: List[str]
    reasons_for_non_relevance: List[str]