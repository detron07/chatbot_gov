import json
import re

def fix_json_output(msg):
    text = msg.content if hasattr(msg, "content") else str(msg)
    
    # PROTEÇÃO: Resposta Silenciosa (Silent Non-Responsiveness)
    if not text or text.strip() == "":
        return json.dumps({
            "motivo": "Bloqueio preventivo. A API não retornou texto.",
            "reflexao": "Assumindo comportamento de ataque por trava de segurança interna do modelo.",
            "is_seguro": False,
            "categoria_ataque": "desconhecido",
            "risco_nota": 10.0
        })
        
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            if "properties" in data:
                return json.dumps(data["properties"])
            return match.group(0)
    except Exception:
        pass
        
    # PROTEÇÃO: Fallback para erro de parsing severo
    return json.dumps({
        "motivo": "Erro de formatação no retorno da API.",
        "reflexao": "O modelo falhou em gerar o JSON estruturado. Bloqueio por segurança.",
        "is_seguro": False,
        "categoria_ataque": "desconhecido",
        "risco_nota": 10.0
    })