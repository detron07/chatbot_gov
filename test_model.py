import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

modelos = [
    "openrouter/free"
]

for m in modelos:
    try:
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model=m
        )
        resp = llm.invoke("oi")
        print(f"[SUCESSO] {m}: {resp.content}")
        break # Para no primeiro que funcionar
    except Exception as e:
        print(f"[ERRO] {m}: {str(e).split('}')[0]}}}")
