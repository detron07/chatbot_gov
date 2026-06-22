from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class AvaliacaoSegurancaEntrada(BaseModel):
    motivo: str = Field(description="Explicação passo a passo do raciocínio.")
    is_seguro: bool = Field(description="True se a entrada for segura. False se for ataque malicioso.")
    categoria_ataque: str = Field(description="Se for ataque, retorne exato: 'eng_social', 'dados_pessoais' ou 'jailbreak'. Se seguro, retorne 'nenhum'.")
    risco_nota: float = Field(description="Nota de 0.0 a 10.0.")

parser_entrada = PydanticOutputParser(pydantic_object=AvaliacaoSegurancaEntrada)

class AvaliacaoSegurancaSaida(BaseModel):
    motivo: str = Field(description="Explicação do raciocínio.")
    is_seguro: bool = Field(description="True se não vazar dados sensíveis, False se vazar.")
    risco_nota: float = Field(description="Nota de 0.0 a 10.0.")

parser_saida = PydanticOutputParser(pydantic_object=AvaliacaoSegurancaSaida)
