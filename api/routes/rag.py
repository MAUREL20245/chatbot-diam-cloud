from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from src.rag import RAGSystem
from src.config import CONFIG
import tempfile
import os

router = APIRouter()

# Instance unique du RAG
rag = RAGSystem(model=CONFIG["model"])


# Modèles de données
class RAGRequest(BaseModel):
    question: str


class RAGResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/ask", response_model=RAGResponse)
def ask(request: RAGRequest):
    """
    Poser une question sur les documents indexés.
    """
    result = rag.ask(request.question)
    return RAGResponse(
        answer=result["answer"],
        sources=result["sources"]
    )


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
    Uploader et indexer un document (PDF ou TXT).
    """
    # Vérifier le format
    if not file.filename.endswith((".pdf", ".txt")):
        return {"error": "Format non supporté. PDF ou TXT uniquement."}

    # Sauvegarder temporairement
    suffix = ".pdf" if file.filename.endswith(".pdf") else ".txt"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Indexer
    nb_chunks = rag.index_document(tmp_path)
    os.unlink(tmp_path)

    return {
        "message": f"{file.filename} indexé avec succès",
        "chunks": nb_chunks
    }


@router.post("/reset")
def reset():
    """
    Supprimer tous les documents indexés.
    """
    rag.reset()
    return {"message": "Base vectorielle réinitialisée"}