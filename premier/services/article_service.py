import os
import requests
from fastapi import HTTPException
from premier.services.oauth_service import OAuthService

class ArticleService:
    def __init__(self):
        self.oauth = OAuthService()
        

    def search_articles_by_keywords(self, keyword):
        url = os.getenv("BASE_URL") + "/published-data/search"
        params = {"q": keyword}
        
        try:
            response = requests.get(url, params=params, headers=self._headers())
            json = response.json()
            return self._fetchArticleIds(json)
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail="Error in fetching articles")

    def fetch_abstract(self, articleId):
        url = os.getenv("BASE_URL") + f"/published-data/publication/docdb/{articleId}/full-cycle"
        print(url)
        try:
            response = requests.get(url, headers=self._headers())
            json = response.json()
            
            title = self._fetchTitle(json)
            abstract = self._fetchAbstract(json)
            return {"id": articleId,"title": title, "abstract": abstract}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail="Error in fetching articles")
        
    def _fetchTitle(self, json) -> str:
        titles = (
                json
                    .get("ops:world-patent-data", {})
                    .get("exchange-documents", {})
                    .get("exchange-document", {})
                    .get("bibliographic-data", {})
                    .get("invention-title", {})
                )
        if isinstance(titles, list):
            return next((item.get("$") for item in titles if item.get("@lang") == "en"), titles[0].get("$", "Title not available"))
        else:
            return titles.get("$", "Title not available")
    
    def _fetchAbstract(self, json) -> str:
        abstracts = (
                json
                    .get("ops:world-patent-data", {})
                    .get("exchange-documents", {})
                    .get("exchange-document", {})
                    .get("abstract", {})
                )
        if isinstance(abstracts, list):
            return next((item.get("p", {}).get("$", "") for item in abstracts if item.get("@lang") == "en"), abstracts[0].get("p", {}).get("$", ""))
        else:
            return abstracts.get("p", {}).get("$", "")
        
    def _fetchArticleIds(self, json) -> list[str]:
        publications = (json
                .get("ops:world-patent-data", {})
                .get("ops:biblio-search", {})
                .get("ops:search-result", {})
                .get("ops:publication-reference", {}))
        
        concatenatedList = []

        for pub in publications:
            doc_id = pub.get("document-id", "")
            country = doc_id.get("country", {}).get("$", "")
            doc_number = doc_id.get("doc-number", {}).get("$", "")
            kind = doc_id.get("kind", {}).get("$", "")
            concatenatedString = f"{country}{doc_number}{kind}"
            concatenatedList.append(concatenatedString)
        return concatenatedList
    
    def _headers(self):
        token = self.oauth.get_access_token()
        return {"Authorization": f"Bearer {token}",
                   "Accept": "application/json"}