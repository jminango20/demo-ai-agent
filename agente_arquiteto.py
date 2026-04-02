import json
from datetime import datetime
from openai import OpenAI

# ---------------- Configuração LLM ----------------
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "mistral:latest"
MEMORIA_ARQUIVO = "memoria_agente.json"

SYSTEM_PROMPT = """
# TODO: definir o papel do agente arquiteto
"""

# ---------------- LLM ----------------
def chamar_llm(prompt):
    resposta = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return resposta.choices[0].message.content

# ---------------- Memória ----------------
def carregar_memoria():
    try:
        with open(MEMORIA_ARQUIVO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_memoria(memoria):
    with open(MEMORIA_ARQUIVO, "w") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

# ---------------- Tools ----------------
def exportar_markdown(arquitetura):
    nome_arquivo = arquitetura["projeto"].replace(" ", "_") + ".md"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"""
# Arquitetura do Projeto

## 📌 Projeto
{arquitetura['projeto']}

## 🕒 Data de Criação
{arquitetura['criacao']}

## 🧩 Arquitetura Sugerida
{arquitetura['arquitetura_sugerida']}
""")
    return nome_arquivo

# ---------------- Tools ----------------
def gerar_topicos_arquitetura(projeto):
    # TODO: Implementar tool do agente
    pass

# ---------------- Agente ----------------
def agente_arquiteto(projeto):
    # TODO: implementar lógica do agente
    pass

# ---------------- Execução ----------------
if __name__ == "__main__":
    projetos = [
        "Criar painel de BI para acompanhamento de vendas usando Power BI e Data Lake",
        "Criar pipeline de Machine Learning na Azure com Azure ML, Data Lake e Feature Store"
    ]

    for projeto in projetos:
        print("\n==============================\n")
        resultado = agente_arquiteto(projeto)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
