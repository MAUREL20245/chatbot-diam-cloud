import ollama
from rich.console import Console
from rich.panel import Panel

console = Console()


class ChatBot:
    """
    Chatbot local basé sur Ollama.
    
    Architecture :
    - self.history : mémoire de la conversation (liste de messages)
    - Chaque message = {"role": "user"/"assistant", "content": "..."}
    - On envoie TOUT l'historique à chaque requête → c'est ainsi que le LLM
      "se souvient" de la conversation
    """

    def __init__(self, config: dict):
        self.model = config["model"]
        self.temperature = config["temperature"]
        self.system_prompt = config["system_prompt"]
        self.history = []  # Mémoire de la conversation

    def chat(self, user_message: str) -> str:
        # 1. Ajouter le message utilisateur à l'historique
        self.history.append({
            "role": "user",
            "content": user_message
        })

        # 2. Appel au LLM via Ollama
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.history
            ],
            options={"temperature": self.temperature}
        )

        # 3. Extraire la réponse
        assistant_message = response["message"]["content"]

        # 4. Sauvegarder dans l'historique
        self.history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset(self):
        """Effacer la mémoire de la conversation"""
        self.history = []
        console.print("[yellow]Conversation réinitialisée.[/yellow]")

    def show_history(self):
        """Afficher l'historique complet"""
        for msg in self.history:
            role = "🧑 Toi" if msg["role"] == "user" else "🤖 Assistant"
            console.print(f"[bold]{role}:[/bold] {msg['content']}\n")