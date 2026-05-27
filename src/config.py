CONFIG = {
    "model": "llama3.2:3b",
    "temperature": 0.7,
    "embedding_model": "all-minilm",
    "system_prompt": """Tu es un assistant IA utile et concis. 
    Tu réponds toujours en français sauf si on te parle autrement.""",

    # Paramètres RAG
    "chunk_size": 200,
    "chunk_overlap": 20,
    "k": 6,
}