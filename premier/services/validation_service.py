import json
import os
import re
from langchain_ollama import ChatOllama

from premier.models.keyword import KeywordCollection, KeywordSet
from premier.models.validation import Validation
from premier.utils.prompt_utils import load_prompt

class ValidationService:
    llm = ChatOllama(
            model = "llama3.2:latest",
            temperature = 0.8,
            num_predict = 256,
        )

    def validate_abstract(self, abstract: str, keyword: str, attempts: int = 5) -> dict:
        prompt = load_prompt('validation.txt')
        messages = [
            ("system", prompt),
            ("human", f"abstract: {abstract}\nkeyword: {keyword}"),
            ]
        try:
            inputString = self.llm.invoke(messages).content
            data = json.loads(inputString)
            validation = Validation(**data)
            print(validation)
            return validation
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"Error occurred: {e}")
        attempts -= 1
        if attempts > 0:
            print(f"Retrying... Remaining attempts: {attempts}")
            return self.validate_abstract(abstract, keyword, attempts)
        else:
            print("Max attempts reached. Raising exception.")
            raise