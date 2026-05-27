from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from src.config import CONFIG
from src.rag import RAGSystem
from datetime import datetime
import math
import re

# ── Outils ───────────────────────────────────────────────────────

def calculatrice(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return f"Résultat : {result}"
    except Exception as e:
        return f"Erreur : {str(e)}"

def date_heure(query: str) -> str:
    now = datetime.now()
    return f"Nous sommes le {now.strftime('%A %d %B %Y')} à {now.strftime('%H:%M')}"

def recherche_doc(question: str) -> str:
    rag = RAGSystem(model=CONFIG["model"])
    result = rag.ask(question)
    return result["answer"]

search = DuckDuckGoSearchRun()

TOOLS = {
    "calculatrice": calculatrice,
    "date_heure": date_heure,
    "recherche_web": search.run,
    "recherche_doc": recherche_doc,
}

TOOLS_DESCRIPTION = """
- calculatrice : faire des calculs. Ex: '2 + 2', 'sqrt(16)', '15 * 85000 / 100'
- date_heure : connaître la date et l'heure actuelle
- recherche_web : chercher des infos récentes sur internet
- recherche_doc : chercher dans les documents PDF indexés
"""

# ── Prompt ReAct ─────────────────────────────────────────────────

REACT_PROMPT = """Tu es un assistant IA. Tu DOIS obligatoirement utiliser un outil avant de répondre.
Tu réponds TOUJOURS en français.

Outils disponibles :
{tools}

RÈGLE ABSOLUE : Tu ne peux JAMAIS répondre directement sans passer par un outil.
Même si tu penses connaître la réponse, tu DOIS utiliser l'outil correspondant.

Format OBLIGATOIRE à respecter :

Thought: réfléchis à quel outil utiliser
Action: nom_exact_de_l_outil
Action Input: ce que tu passes à l_outil
Observation: [le système mettra le résultat ici]
Thought: j'ai le résultat
Final Answer: ta réponse en français

IMPORTANT :
- Pour l'heure ou la date → utilise OBLIGATOIREMENT date_heure
- Pour un calcul → utilise OBLIGATOIREMENT calculatrice
- Pour une actualité → utilise OBLIGATOIREMENT recherche_web
- Pour les documents → utilise OBLIGATOIREMENT recherche_doc

Question : {question}
"""

# ── Boucle ReAct manuelle ─────────────────────────────────────────

class AIAgent:
    """
    Agent IA avec boucle ReAct manuelle.
    
    Thought  → L'agent réfléchit
    Action   → L'agent choisit un outil
    Observation → On exécute l'outil et on donne le résultat
    Final Answer → L'agent répond
    """

    def __init__(self):
        self.llm = OllamaLLM(
            model=CONFIG["model"],
            temperature=0.1
        )

    def run(self, question: str) -> str:
        prompt = REACT_PROMPT.format(
            tools=TOOLS_DESCRIPTION,
            question=question
        )

        for i in range(5):
            response = self.llm.invoke(prompt, stop=["Observation:"])
            print(f"\n--- Itération {i+1} ---\n{response}")

            # L'agent a une réponse finale ?
            if "Final Answer:" in response:
                return response.split("Final Answer:")[-1].strip()

            # L'agent veut utiliser un outil ?
            action_match = re.search(r"Action:\s*(\w+)", response)
            input_match = re.search(r"Action Input:\s*(.+)", response)

            if action_match and input_match:
                tool_name = action_match.group(1).strip()

                # Nettoyer l'input
                tool_input = input_match.group(1).strip().strip("'\"")

                # Si l'input est vide ou inutile → utiliser la question originale
                if not tool_input or "None" in tool_input or "je vais" in tool_input.lower():
                    tool_input = question

                if tool_name in TOOLS:
                    observation = TOOLS[tool_name](tool_input)
                else:
                    observation = f"Outil '{tool_name}' inconnu."

                print(f"Outil : {tool_name} | Input : {tool_input}")
                print(f"Observation : {observation}")

                # Enrichir le prompt ET forcer Final Answer
                prompt += f"\n{response}\nObservation: {observation}\nThought: J'ai le résultat, je formule la réponse finale.\nFinal Answer:"

                # Demander directement la réponse finale
                final = self.llm.invoke(prompt)
                return final.strip()
            else:
                return response

        return "Je n'ai pas pu trouver une réponse après 5 tentatives."