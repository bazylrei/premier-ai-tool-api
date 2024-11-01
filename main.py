from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from premier.services.article_service import ArticleService
from premier.services.keyword_service import KeywordService
from premier.services.oauth_service import OAuthService
from premier.services.validation_service import ValidationService


load_dotenv()
app = FastAPI()
articleService = ArticleService()
oauthService = OAuthService()
keywordService = KeywordService()
validationService = ValidationService()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/auth")
async def auth():
    token = oauthService.get_access_token()
    print(token)
    return token

@app.get("/generate_keywords/{keyword}")
async def generate_keywords(keyword: str):
    return keywordService.get_similar_keywords(keyword)

@app.get("/search_articles/{keyword}")
async def search_articles(keyword: str):
    articleIds = articleService.search_articles_by_keywords(keyword)
    articles = []
    # for articleId in articleIds:
    # articleInfo = articleService.fetch_abstract(articleId)
    articleInfo = articleService.fetch_abstract(articleIds[0])
    abstract = articleInfo.get("abstract")
    validationService.validate_abstract(abstract, keyword)
    articles.append(articleInfo)
    return articles

@app.get("/fetch_abstracts/{article_id}")
async def fetch_abstracts(article_id: str):
    return articleService.fetch_abstract(article_id)

# @app.get("/evaluate_relevance")
# async def evaluate_relevance(abstracts: List[Dict]):
#     return await relevance_service.evaluate_abstracts(abstracts)

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    