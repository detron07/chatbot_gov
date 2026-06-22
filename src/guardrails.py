from langchain_core.runnables import RunnableLambda
from src.config import cache_manager

def avaliar_cache(x):
    if not cache_manager:
        return {"cache_seguro": True, "pergunta": x["pergunta"]}
        
    pergunta = x["pergunta"]
    seguro, categoria = cache_manager.verificar_ataque(pergunta)
    
    if not seguro:
        return {"cache_seguro": False, "categoria": categoria, "pergunta": pergunta}
        
    return {"cache_seguro": True, "pergunta": pergunta}

camada_0 = RunnableLambda(avaliar_cache)

def is_entrada_segura(entrada):
    pergunta = entrada["pergunta"]
    avaliacao = entrada["avaliacao"]
    
    if not avaliacao.is_seguro and avaliacao.risco_nota > 6.0:
        categoria = avaliacao.categoria_ataque if avaliacao.categoria_ataque in ['eng_social', 'dados_pessoais', 'jailbreak'] else 'desconhecido'
        if cache_manager: 
            cache_manager.registrar_ataque(pergunta, categoria, risco_nota=avaliacao.risco_nota, motivo=avaliacao.motivo)
        return False
        
    return True

def is_saida_segura(saida):
    pergunta = saida["pergunta"]
    avaliacao = saida["avaliacao_saida"]
    
    if not avaliacao.is_seguro and avaliacao.risco_nota > 6.0:
        if cache_manager: 
            cache_manager.registrar_ataque(pergunta, "vazamento_dados", risco_nota=avaliacao.risco_nota, motivo=avaliacao.motivo, origem="llm_judge_saida")
        return False
        
    return True
