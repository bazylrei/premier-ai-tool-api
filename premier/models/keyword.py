from pydantic import BaseModel
from typing import List

class KeywordSet(BaseModel):
    keywords: List[str]

class KeywordCollection(BaseModel):
    keywordSets: List[KeywordSet]