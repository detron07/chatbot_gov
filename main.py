import os
from src.chains import chain_completa # Ajuste o nome da variável importada conforme o seu código

# Limite estabelecido para mitigar ataques de saturação de contexto (Long Prompts)
LIMITE_CARACTERES = 800

def processar_pergunta(pergunta_usuario: str) -> str:
    """
    Processa a entrada do usuário aplicando validações estruturais preliminares 
    antes de acionar o pipeline de inteligência artificial.
    """
    # PROTEÇÃO: Bloqueio contra saturação de limite de tokens/caracteres
    if len(pergunta_usuario) > LIMITE_CARACTERES:
        return f"[BLOQUEIO DE SEGURANÇA] A sua mensagem excede o limite de {LIMITE_CARACTERES} caracteres. Por favor, seja mais objetivo."
    
    try:
        # Aciona o fluxo de Guardrails e geração de resposta
        resposta_final = chain_completa.invoke({"pergunta": pergunta_usuario})
        return resposta_final
    except Exception as e:
        return f"[ERRO NO SISTEMA] Não foi possível processar a requisição: {str(e)}"

def main():
    print("="*50)
    print("Chatbot Governamental Seguro Iniciado.")
    print("Digite 'sair' para encerrar o sistema.")
    print("="*50)
    
    while True:
        pergunta = input("\nCidadão: ")
        
        if pergunta.lower().strip() in ['sair', 'exit', 'quit']:
            print("Encerrando sistema...")
            break
            
        resposta = processar_pergunta(pergunta)
        print(f"\nAssistente: {resposta}")

if __name__ == "__main__":
    main()