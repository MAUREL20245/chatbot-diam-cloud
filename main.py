from src.chatbot import ChatBot
from src.config import CONFIG
from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]Chatbot IA Local[/bold cyan]\n"
        f"Modèle : [green]{CONFIG['model']}[/green]\n"
        "Commandes : [yellow]/reset[/yellow] | [yellow]/history[/yellow] | [yellow]/quit[/yellow]",
        title="🤖 Club D.I.A.M"
    ))

    bot = ChatBot(CONFIG)

    while True:
        try:
            user_input = console.input("\n[bold cyan]Toi >[/bold cyan] ").strip()

            if not user_input:
                continue

            if user_input == "/quit":
                console.print("[red]Au revoir ![/red]")
                break
            elif user_input == "/reset":
                bot.reset()
                continue
            elif user_input == "/history":
                bot.show_history()
                continue

            console.print("\n[bold green]Assistant >[/bold green]", end=" ")
            response = bot.chat(user_input)
            console.print(response)

        except KeyboardInterrupt:
            console.print("\n[red]Interruption. Au revoir ![/red]")
            break


if __name__ == "__main__":
    main()