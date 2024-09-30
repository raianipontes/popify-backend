from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from service.rag_pipeline import RAGService
import logging

app = FastAPI()
logger = logging.getLogger(__name__)


# Configuração de CORS (se necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria uma instância do serviço RAG
service = RAGService()

# Armazena as mensagens em uma lista para simular um banco de dados (você pode trocar isso por um banco de dados real)
messages = []

@app.post("/messages/")
async def create_message(request: Request):
    data = await request.json()
    logger.info(f"Dados recebidos: {data}")
    user_query = data.get('message')

    try:
        # Gera a resposta do bot
        bot_response = service.generate_answer(user_query)
        logger.info(f"Resposta gerada: {bot_response}")

        # Armazena a mensagem do usuário e a resposta do bot
        messages.append({"content": user_query, "sender": "user"})
        messages.append({"content": bot_response, "sender": "bot"})

        return {"response": bot_response}
    except Exception as e:
        logger.error(f"Erro ao processar a mensagem: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/messages/")
async def get_messages():
    try:
        # Retorna todas as mensagens armazenadas
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
