# 🧠 Agent IA Cloud — Club D.I.A.M

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Groq](https://img.shields.io/badge/Groq-Cloud%20LLM-orange)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-green)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![LangChain](https://img.shields.io/badge/LangChain-RAG-FFD700)
![Render](https://img.shields.io/badge/Render-Deployed-purple)

> Agent IA complet construit progressivement dans le cadre du **Club D.I.A.M** —
> Du chatbot local à l'agent IA autonome déployé sur le cloud, avec RAG, recherche web et API REST.

🌍 **Demo Live** : [https://chatbot-diam-cloud.onrender.com](https://chatbot-diam-cloud.onrender.com)

---

## 🎯 Vue d'ensemble

Ce projet est une plateforme IA modulaire et évolutive qui combine :

- 💬 **Chatbot conversationnel** basé sur un LLM (local ou cloud)
- 📚 **Système RAG** pour interroger vos propres documents (Pinecone)
- ⚡ **API REST** exposant tous les services (FastAPI)
- 🧠 **Agent IA ReAct** capable de raisonner et d'utiliser des outils
- 🌐 **Recherche web** en temps réel (DuckDuckGo)
- 🐳 **Architecture Docker** pour un déploiement reproductible
- ☁️ **Déployé sur Render** avec Groq comme LLM cloud

---

## 🏗️ Architecture

\`\`\`
chatbot-diam-cloud/
├── src/
│   ├── config.py        # Configuration centralisée
│   ├── chatbot.py       # Logique du chatbot (Ollama local / Groq cloud)
│   ├── rag.py           # Système RAG (LangChain + Pinecone)
│   └── agent.py         # Agent IA ReAct (from scratch)
├── api/
│   ├── main.py          # Serveur FastAPI
│   └── routes/
│       ├── chat.py      # Endpoints /chat
│       └── rag.py       # Endpoints /rag
├── app.py               # Interface Streamlit — Chatbot
├── app_rag.py           # Interface Streamlit — RAG
├── app_agent.py         # Interface Streamlit — Agent (déployé)
├── Dockerfile
├── docker-compose.yml
├── Procfile             # Configuration Render
└── requirements.txt
\`\`\`

---

## 🚀 Stack Technologique

| Composant | Local | Cloud | Rôle |
|-----------|-------|-------|------|
| **LLM** | Ollama + llama3.2:3b | Groq + llama-3.3-70b | Génération de texte |
| **Embeddings** | all-minilm | multilingual-e5-large | Vectorisation |
| **Vector DB** | ChromaDB | Pinecone | Stockage des vecteurs |
| **RAG** | LangChain | LangChain | Pipeline RAG |
| **Recherche web** | DuckDuckGo | DuckDuckGo | Infos en temps réel |
| **API** | FastAPI + Uvicorn | FastAPI + Uvicorn | Exposition REST |
| **UI** | Streamlit | Streamlit | Interface utilisateur |
| **Agent** | ReAct (from scratch) | ReAct (from scratch) | Raisonnement + outils |
| **Deploy** | Docker Compose | Render | Orchestration |

---

## ⚙️ Configuration centralisée

\`\`\`python
CONFIG = {
    "mode": "cloud",
    "local_model": "llama3.2:3b",
    "cloud_model": "llama-3.3-70b-versatile",
    "groq_api_key": os.getenv("GROQ_API_KEY"),
    "temperature": 0.7,
    "chunk_size": 700,
    "chunk_overlap": 100,
    "k": 10,
}
\`\`\`

---

## 🐳 Démarrage local

\`\`\`bash
git clone https://github.com/MAUREL20245/chatbot-diam-cloud.git
cd chatbot-diam-cloud
docker compose up -d
docker exec ollama ollama pull llama3.2:3b
\`\`\`

---

## 🧠 Agent IA — Pattern ReAct

\`\`\`
Question → Thought → Action → Observation → Final Answer
\`\`\`

| Outil | Capacité |
|-------|---------|
| 🧮 calculatrice | Calculs mathématiques |
| 🕐 date_heure | Date et heure actuelle |
| 🌐 recherche_web | Recherche internet (DuckDuckGo) |
| 📄 recherche_doc | Recherche dans les PDFs indexés (Pinecone) |

---

## ☁️ Variables d'environnement Render

\`\`\`
GROQ_API_KEY=votre_clé_groq
PINECONE_API_KEY=votre_clé_pinecone
PYTHON_VERSION=3.11.9
\`\`\`

---

## 📋 Roadmap

- [x] Phase 1 — Chatbot local (Ollama + Python)
- [x] Phase 2 — Interface Streamlit
- [x] Phase 3 — Système RAG (LangChain + ChromaDB)
- [x] Phase 4 — API REST (FastAPI)
- [x] Phase 5 — Agent IA (ReAct from scratch)
- [x] Phase 6 — Dockerisation (5 microservices)
- [x] Phase 7 — Déploiement Cloud (Groq + Pinecone + Render)
- [ ] Phase 8 — Mémoire persistante
- [ ] Phase 9 — Agent autonome complet

---

## 👨‍💻 Auteur

**GUEPIE Aristide Maurel**  
Data Scientist / MLOps Engineer / AI Engineer  
📍 Abidjan, Côte d'Ivoire  
🔗 [Portfolio](https://maurel20245.github.io/chatbot-diam)  
🔗 [LinkedIn](https://www.linkedin.com/in/maurel-guepie-907b2b154/)

---

*"Ne pas juste suivre des tutoriels — comprendre l'architecture, construire progressivement, expérimenter, créer des solutions réelles."*  
**— Club D.I.A.M**
