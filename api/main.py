from fastapi import FastAPI

from dotenv import load_dotenv, find_dotenv
from routers.llm_router import router as llm_router
from routers.operacoes_router import router as operacoes_router
from routers.web_router import router as web_router
from routers.health_router import router as health_router
from fastapi_mcp import FastApiMCP


load_dotenv(find_dotenv())


app = FastAPI(
    title="Aula",
    description="Contém todos os **endpoints** disponíves para serem utilizados",
    summary="API desenvolvida durante a aula de Construção de APIs para IA",
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Rogério Rodrigues Carvalho",
        "url": "http://github.com/rogerior/",
        "email": "rogerior@ufg.br",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    # dependencies=[Depends(common_api_token)],
)

# Inclusão das rotas (endpoints)
app.include_router(router=health_router, tags=["Health Check"])
app.include_router(router=llm_router, tags=["IA"])
app.include_router(router=operacoes_router, tags=["Operações matemáticas"])
app.include_router(router=web_router, tags=["Busca na web"])

mcp = FastApiMCP(app)
mcp.mount_http()
