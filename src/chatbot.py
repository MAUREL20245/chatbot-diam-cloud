from rich.console import Console
from src.config import CONFIG

console = Console()


class ChatBot:
    """
    Chatbot supportant deux modes :
    - local : Ollama (llama3.2:3b)
    - cloud : Groq API (llama3-8b-8192)
    """

    def __init__(self, config: dict):
        self.model = config["model"]
        self.temperature = config["temperature"]
        self.system_prompt = config["system_prompt"]
        self.mode = config["mode"]
        self.history = []

        if self.mode == "cloud":
            from groq import Groq
            self.client = Groq(api_key=config["groq_api_key"])
        else:
            import ollama
            self.client = None

    def chat(self, user_message: str) -> str:
        self.history.append({
            "role": "user",
            "content": user_message
        })

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history
        ]

        if self.mode == "cloud":
            # Appel Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            assistant_message = response.choices[0].message.content
        else:
            # Appel Ollama local
            import ollama
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={"temperature": self.temperature}
            )
            assistant_message = response["message"]["content"]

        self.history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset(self):
        self.history = []
        console.print("[yellow]Conversation réinitialisée.[/yellow]")

    def show_history(self):
        for msg in self.history:
            role = " Toi" if msg["role"] == "user" else "🤖 Assistant"
            console.print(f"[bold]{role}:[/bold] {msg['content']}\n")