from fastapi import APIRouter

from models import (
    WebSearchRequest,
    WebSearchResults,
    ExtractURLRequest,
    ExtractURLResponse,
)
from utils import get_logger
from ddgs import DDGS


logger = get_logger()
router = APIRouter()


@router.post(
    path="/web_search/v1",
    response_model=WebSearchResults,
    summary="Realiza uma busca na web usando DuckDuckGo e retorna os resultados",
    description="Este endpoint realiza uma busca na web usando o mecanismo de busca DuckDuckGo e retorna os resultados encontrados, incluindo data, título, corpo, URL, imagem e fonte de cada notícia.",
)
def web_search(request: WebSearchRequest):

    results = DDGS().news(
        query=request.query, region=request.region, max_results=request.max_results
    )

    return WebSearchResults(results=results)


@router.post(
    path="/extract_url/v1",
    response_model=ExtractURLResponse,
    summary="Extrai o conteúdo de uma URL usando DuckDuckGo",
    description="Este endpoint extrai o conteúdo de uma URL usando o mecanismo de busca DuckDuckGo e retorna o conteúdo extraído.",
)
def extract_url(request: ExtractURLRequest):

    result = DDGS().extract(request.url)

    return ExtractURLResponse(url=request.url, content=result["content"])
