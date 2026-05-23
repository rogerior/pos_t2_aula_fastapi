from fastapi import APIRouter

from models import Historia
from utils import execute_prompt, get_logger


logger = get_logger()
router = APIRouter()


@router.post("/gerar_historia/v1")
def gerar_historia(historia: Historia):
    logger.info(f"Recebido pedido para gerar história com tema: {historia.tema}")

    prompt = f"Escreva uma história sobre o tema: {historia.tema}"

    resposta = execute_prompt(prompt)
    
    logger.info(f"História gerada com sucesso para o tema: {historia.tema}")

    return {"historia": resposta}
