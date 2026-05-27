#  Chatbot IA Local — Club D.I.A.M

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![LangChain](https://img.shields.io/badge/LangChain-RAG-FFD700)

> Système IA complet construit progressivement dans le cadre du **Club D.I.A.M** —  
> Du chatbot local à l'agent IA autonome, en passant par le RAG et l'API REST.

---

##  Vue d'ensemble

Ce projet est une plateforme IA modulaire et évolutive qui combine :

-  **Chatbot conversationnel** basé sur un LLM local
-  **Système RAG** pour interroger vos propres documents
-  **API REST** exposant tous les services
-  **Agent IA** capable de raisonner et d'utiliser des outils
-  **Architecture Docker** pour un déploiement reproductible

**Tout tourne 100% en local — sans cloud, sans clé API, sans coût.**

---

##  Architecture

```
chatbot-diam/
├── src/
│   ├── config.py        # Configuration centralisée
│   ├── chatbot.py       # Logique du chatbot
│   ├── rag.py           # Système RAG (LangChain + ChromaDB)
│   └── agent.py         # Agent IA (ReAct from scratch)
├── api/
│   ├── main.py          # Serveur FastAPI
│   └── routes/
│       ├── chat.py      # Endpoints /chat
│       └── rag.py       # Endpoints /rag
├── app.py               # Interface Streamlit — Chatbot
├── app_rag.py           # Interface Streamlit — RAG
├── app_agent.py         # Interface Streamlit — Agent
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

##  Stack Technologique

| Composant | Technologie | Rôle |
|-----------|------------|------|
| **LLM** | Ollama + llama3.2:3b | Moteur de génération local |
| **Embeddings** | all-minilm | Vectorisation des documents |
| **Vector DB** | ChromaDB | Stockage des vecteurs |
| **RAG** | LangChain | Pipeline Retrieval + Generation |
| **API** | FastAPI + Uvicorn | Exposition REST |
| **UI** | Streamlit | Interface utilisateur |
| **Agent** | ReAct (from scratch) | Raisonnement + outils |
| **Deploy** | Docker Compose | Orchestration des services |

---

##  Démarrage rapide

### Prérequis
- Docker + Docker Compose
- 8 GB RAM minimum

### Lancement

```bash
# Cloner le repo
git clone https://github.com/MAUREL20245/chatbot-diam.git
cd chatbot-diam

# Lancer tous les services
docker compose up -d

# Télécharger le modèle LLM
docker exec ollama ollama pull llama3.2:3b
```

### Accès aux services

| Service | URL | Description |
|---------|-----|-------------|
|  Chatbot | http://localhost:8501 | Chat conversationnel |
|  RAG | http://localhost:8503 | Questions sur documents |
|  Agent | http://localhost:8502 | Agent avec outils |
|  API Docs | http://localhost:8001/docs | Documentation Swagger |

---

##  API REST

### Chat
```bash
curl -X POST http://localhost:8001/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour, qui es-tu ?"}'
```

### RAG — Upload document
```bash
curl -X POST http://localhost:8001/rag/upload \
  -F "file=@mon_document.pdf"
```

### RAG — Question
```bash
curl -X POST http://localhost:8001/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "De quoi parle ce document ?"}'
```

---

##  Agent IA — Pattern ReAct

L'agent utilise le pattern **ReAct (Reasoning + Acting)** implémenté from scratch :

```
Question
   │
   ▼
Thought  → Le LLM réfléchit à l'outil à utiliser
   │
   ▼
Action   → Il choisit l'outil
   │
   ▼
Observation → Python exécute le vrai outil
   │
   ▼
Final Answer → Le LLM formule la réponse
```

### Outils disponibles

| Outil | Capacité |
|-------|---------|
|  calculatrice | Calculs mathématiques |
|  date_heure | Date et heure actuelle |
|  recherche_web | Recherche internet (DuckDuckGo) |
|  recherche_doc | Recherche dans les PDFs indexés |

---

##  Configuration

Toute la configuration est centralisée dans `src/config.py` :

```python
CONFIG = {
    "model": "llama3.2:3b",          # Modèle LLM
    "temperature": 0.7,               # Créativité
    "embedding_model": "all-minilm",  # Modèle embeddings
    "chunk_size": 200,                # Taille des chunks RAG
    "chunk_overlap": 20,              # Chevauchement
    "k": 6,                           # Chunks récupérés
}
```

---

##  Roadmap

- [x] Phase 1 — Chatbot local (Ollama + Python)
- [x] Phase 2 — Interface Streamlit
- [x] Phase 3 — Système RAG (LangChain + ChromaDB)
- [x] Phase 4 — API REST (FastAPI)
- [x] Phase 5 — Agent IA (ReAct from scratch)
- [x] Phase 6 — Dockerisation
- [ ] Phase 7 — Déploiement Cloud

---

##  Auteur

**GUEPIE Aristide Maurel**  
Data Scientist / MLOps Engineer  
Abidjan, Côte d'Ivoire

---

##  Contexte

Projet développé dans le cadre du **Club D.I.A.M** — groupe de mentors spécialisés en IA,  
avec pour objectif de former la prochaine génération d'**AI Engineers** en Côte d'Ivoire.

---

*"Ne pas juste suivre des tutoriels — comprendre l'architecture, construire progressivement, expérimenter, créer des solutions réelles."*  
**— Club D.I.A.M**