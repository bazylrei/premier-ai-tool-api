import json
import os
import re
from langchain_ollama import ChatOllama

from premier.models.keyword import KeywordCollection, KeywordSet
from premier.utils.prompt_utils import load_prompt

class KeywordService:
    llm = ChatOllama(
            model = "llama3.2:latest",
            temperature = 0.8,
            num_predict = 256,
        )

    def get_similar_keywords(self, keyword: str, attempts: int = 5) -> dict:
        prompt = load_prompt('keywords.txt')
        messages = [
            ("system", prompt),
            ("human", keyword),
            ]
        try:
            input_string = self.llm.invoke(messages).content
            keywords_array = json.loads(input_string)
            keywordCollection = KeywordCollection(keywordSets = [])
            for keyword in keywords_array:
                matches = re.findall(r'"([^"]+)"', keyword)
                keywordSet = KeywordSet(keywords = matches)
                keywordCollection.keywordSets.append(keywordSet)
            return keywordCollection
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"Error occurred: {e}")
        attempts -= 1
        if attempts > 0:
            print(f"Retrying... Remaining attempts: {attempts}")
            return self.get_similar_keywords(keyword, attempts)
        else:
            print("Max attempts reached. Raising exception.")
            raise