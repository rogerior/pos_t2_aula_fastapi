from fastapi import FastAPI, Depends

from dotenv import load_dotenv, find_dotenv
from utils import common_api_token
from routers.llm_router import router as llm_router
from routers.operacoes_router import router as operacoes_router


load_dotenv(find_dotenv())


app = FastAPI(
    title="Aula",
    description="Contém todos os **endpoints** disponíves para serem utilizados",
    summary="API desenvolvida durante a aula de Construção de APIs para IA, utilizando FastAPI",
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
    dependencies=[Depends(common_api_token)],
)

# Inclusão das rotas (endpoints)
app.include_router(router=llm_router, tags=["IA"])
app.include_router(router=operacoes_router, tags=["Operações matemáticas"])
