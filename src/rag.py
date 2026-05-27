from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

from src.config import CONFIG

CHROMA_PATH = "/media/maurel/disk2/projets/chatbot-local/chroma_db"


class RAGSystem:
    """
    Système RAG (Retrieval Augmented Generation)

    Architecture :
    1. INDEXATION  : Document → Chunks → Vecteurs → ChromaDB
    2. RECHERCHE   : Question → Vecteur → Chunks similaires
    3. GÉNÉRATION  : Chunks + Question → LLM → Réponse
    """

    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        self.embeddings = OllamaEmbeddings(model=CONFIG["embedding_model"]) 
        self.llm = OllamaLLM(model=model)
        self.vectorstore = None

        if os.path.exists(CHROMA_PATH):
            self.vectorstore = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=self.embeddings
            )

    def load_document(self, file_path: str) -> list:
        """Charger un document (PDF ou TXT)"""
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError("Format non supporté. Utilise PDF ou TXT.")
        return loader.load()

    def index_document(self, file_path: str) -> int:
        """Indexer un document dans ChromaDB."""
        documents = self.load_document(file_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CONFIG["chunk_size"],
            chunk_overlap=CONFIG["chunk_overlap"],
        )
        chunks = splitter.split_documents(documents)

        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=CHROMA_PATH
            )
        else:
            self.vectorstore.add_documents(chunks)

        return len(chunks)

    def ask(self, question: str) -> dict:
        """Poser une question sur les documents indexés."""
        if self.vectorstore is None:
            return {
                "answer": "Aucun document indexé. Charge d'abord un document.",
                "sources": []
            }

        # Prompt RAG
        prompt = ChatPromptTemplate.from_template("""
Tu es un assistant qui répond aux questions en te basant uniquement sur le contexte fourni.
Si la réponse n'est pas dans le contexte, dis-le clairement.

Contexte :
{context}

Question : {question}

Réponse :""")

        # Retriever
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": CONFIG["k"]}
        )

        # Pipeline LCEL moderne
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        answer = chain.invoke(question)

        # Récupérer les sources
        source_docs = retriever.invoke(question)
        sources = []
        for doc in source_docs:
            source = doc.metadata.get("source", "inconnu")
            page = doc.metadata.get("page", "")
            sources.append(
                f"{os.path.basename(source)}" +
                (f" (page {page+1})" if page != "" else "")
            )

        return {
            "answer": answer,
            "sources": list(set(sources))
        }

    def reset(self):
        """Supprimer tous les documents indexés"""
        import shutil
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            self.vectorstore = None