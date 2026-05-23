from fastapi import status, HTTPException
import logging
from groq import Groq
import os


API_TOKEN = str(os.getenv("API_TOKEN"))


def get_logger():
    """
    Configura e retorna uma instância do logger da aplicação.

    Returns:
        logging.Logger: Instância do logger configurada com nível INFO
        e formato de mensagem com data/hora, nível e conteúdo.
    """

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("fastapi")

    return logger


def common_api_token(api_token: str):
    """
    Valida o token de autenticação da API.

    Args:
        api_token (str): Token de autenticação fornecido na requisição.

    Raises:
        HTTPException: Retorna status 401 (UNAUTHORIZED) se o token
        fornecido não corresponder ao token configurado na variável
        de ambiente API_TOKEN.

    Returns:
        dict: Dicionário contendo o token validado no formato
        ``{"api_token": api_token}``.
    """
    logger = get_logger()
    logger.info(f"Token recebido: {api_token}")

    if api_token != API_TOKEN:
        logger.warning("Token de autenticação inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
        )

    logger.info("Token de autenticação válido")
    return {"api_token": api_token}


def execute_prompt(prompt: str, model: str = "llama-3.1-8b-instant"):
    """
    Envia um prompt para o modelo LLM via API Groq e retorna a resposta.

    Args:
        prompt (str): Texto do prompt a ser enviado ao modelo.
        model (str, optional): Identificador do modelo a ser utilizado.
            Padrão: ``"llama-3.1-8b-instant"``.

    Returns:
        str: Conteúdo da resposta gerada pelo modelo.
    """
    logger = get_logger()
    logger.info(f"Iniciando execução de prompt. Modelo: {model}. Prompt recebido: {prompt}")

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )

    resultado = chat_completion.choices[0].message.content
    logger.info(f"Resposta gerada: {resultado}")
    logger.info(f"Tokens utilizados: {chat_completion.usage.total_tokens}")

    return resultado
