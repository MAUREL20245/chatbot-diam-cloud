from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, rag

# Création de l'application FastAPI
app = FastAPI(
    title="Chatbot IA Local — Club D.I.A.M",
    description="API REST pour le chatbot IA local avec RAG",
    version="1.0.0"
)

# CORS — permet à Streamlit d'appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routes
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])


@app.get("/")
def root():
    return {
        "message": "Chatbot IA Local — Club D.I.A.M",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "ok"}