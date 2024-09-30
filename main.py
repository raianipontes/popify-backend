from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from service.rag_pipeline import RAGService
import logging

app = FastAPI()
logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = RAGService()

messages = []

@app.post("/messages/")
async def create_message(request: Request):
    data = await request.json()
    logger.info(f"Dados recebidos: {data}")
    user_query = data.get('message')

    try:
        bot_response = service.generate_answer(user_query)
        logger.info(f"Resposta gerada: {bot_response}")

        messages.append({"content": user_query, "sender": "user"})
        messages.append({"content": bot_response, "sender": "bot"})

        return {"response": bot_response}
    except Exception as e:
        logger.error(f"Erro ao processar a mensagem: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/messages/")
async def get_messages():
    try:
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
