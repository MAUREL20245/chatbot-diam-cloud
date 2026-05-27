from fastapi import APIRouter
from pydantic import BaseModel
from src.chatbot import ChatBot
from src.config import CONFIG

router = APIRouter()

# Instance unique du chatbot (partagée entre les requêtes)
chatbot = ChatBot(CONFIG)


# Modèles de données (ce que l'API reçoit et renvoie)
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    model: str


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Envoyer un message au chatbot et recevoir une réponse.
    """
    response = chatbot.chat(request.message)
    return ChatResponse(
        response=response,
        model=CONFIG["model"]
    )


@router.post("/reset")
def reset():
    """
    Réinitialiser la mémoire du chatbot.
    """
    chatbot.reset()
    return {"message": "Conversation réinitialisée"}


@router.get("/history")
def history():
    """
    Récupérer l'historique de la conversation.
    """
    return {"history": chatbot.history}