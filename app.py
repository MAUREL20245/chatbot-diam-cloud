import streamlit as st
from src.chatbot import ChatBot
from src.config import CONFIG

# ── Configuration de la page ──────────────────────────────────────
st.set_page_config(
    page_title="Chatbot IA Local — Club D.I.A.M",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Chatbot IA Local")
st.caption(f"Modèle : `{CONFIG['model']}` — Propulsé par Ollama")

# ── Initialisation de la session ──────────────────────────────────
# st.session_state persiste entre les interactions utilisateur
# C'est ainsi qu'on garde la mémoire de la conversation dans Streamlit

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBot(CONFIG)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Affichage de l'historique ─────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Zone de saisie ────────────────────────────────────────────────
if prompt := st.chat_input("Pose ta question ici..."):

    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)

    # Sauvegarder dans l'historique visuel
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Obtenir la réponse du chatbot
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            response = st.session_state.chatbot.chat(prompt)
        st.markdown(response)

    # Sauvegarder la réponse dans l'historique visuel
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ── Bouton Reset dans la sidebar ─────────────────────────────────
with st.sidebar:
    st.header("⚙️ Contrôles")   
    st.info(f"**Modèle :** {CONFIG['model']}\n\n**Température :** {CONFIG['temperature']}")

    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.chatbot.reset()
        st.session_state.messages = []
        st.rerun()