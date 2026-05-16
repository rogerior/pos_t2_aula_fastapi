from enum import Enum

from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field


API_TOKEN = "123"

def common_api_token(api_token: str):
    
    if api_token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autenticação inválido")
    
    return {"api_token": api_token}


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
    dependencies=[Depends(common_api_token)]
)



@app.get("/teste")
def hello_world():
    return {"mensagem": "Hello World"}


# http://127.0.0.1:8000/soma/3/2
@app.post("/soma/v1/{numero1}/{numero2}", tags=["Operações matemáticas"], deprecated=True, summary="Será descontinuado em 15/06")
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# http://127.0.0.1:8000/soma_formato2?numero1=3&numero2=2
@app.post("/soma/v2", tags=["Operações matemáticas"])
def soma_formato2(numero1: int, numero2: int, api_token: str):
    
    if api_token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autenticação inválido")
    
    total = numero1 + numero2
    return {"resultado": total}


class Numeros(BaseModel):
    numero1: int = Field(5, description="O primeiro número a ser somado")
    numero2: int = Field(3, description="O segundo número a ser somado")


class Resultado(BaseModel):
    resultado: int = Field(..., description="O resultado da soma dos dois números")




# 'http://127.0.0.1:8000/soma_formato3'
#   -d '{
#   "numero1": 3,
#   "numero2": 2
# }'
@app.post("/soma/v3", 
        response_model=Resultado, 
        summary="Soma de dois números utilizando um modelo de dados",
        description="Este endpoint recebe um modelo de dados contendo dois números e retorna o resultado da soma desses números.",
        tags=["Operações matemáticas"],
        status_code=status.HTTP_200_OK,
        response_description="Processamento realizado com sucesso"
        )
def soma_formato3(numeros: Numeros):
    
    # Se o numero1 for negativo, retorna um erro
    if numeros.numero1 < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O número 1 não pode ser negativo")
    
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}



class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


@app.post("/operacao_matematica", tags=["Operações matemáticas"])
def operacao_matematica(numeros: Numeros, operacao: TipoOperacao):
    
    if operacao == TipoOperacao.soma:
        resultado = numeros.numero1 + numeros.numero2
    
    elif operacao == TipoOperacao.subtracao:
        resultado = numeros.numero1 - numeros.numero2
    
    elif operacao == TipoOperacao.multiplicacao:
        resultado = numeros.numero1 * numeros.numero2
    
    elif operacao == TipoOperacao.divisao:
        resultado = numeros.numero1 / numeros.numero2
    
    return {"resultado": resultado}
