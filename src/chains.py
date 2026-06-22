from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from src.config import llm_juiz, llm_principal
from src.models import parser_entrada, parser_saida
from src.prompts import template_juiz_unico, template_saida, template_geracao
from src.utils import fix_json_output

llm_juiz_fixed = llm_juiz | RunnableLambda(fix_json_output)

chain_juiz_entrada = PromptTemplate(
    template=template_juiz_unico,
    input_variables=["pergunta"],
    partial_variables={"instrucoes_formato": parser_entrada.get_format_instructions()}
) | llm_juiz_fixed | parser_entrada

chain_juiz_saida = PromptTemplate(
    template=template_saida,
    input_variables=["pergunta", "resposta_llm"],
    partial_variables={"instrucoes_formato": parser_saida.get_format_instructions()}
) | llm_juiz_fixed | parser_saida

chain_geracao = (
    PromptTemplate.from_template(template_geracao)
    | llm_principal
    | (lambda msg: msg.content)
)
