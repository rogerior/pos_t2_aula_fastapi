from fastapi import APIRouter

from models import Historia
from utils import execute_prompt


router = APIRouter()


@router.post("/gerar_historia/v1")
def gerar_historia(historia: Historia):

    prompt = f"Escreva uma história sobre o tema: {historia.tema}"

    historia = execute_prompt(prompt)

    return {"historia": historia}
