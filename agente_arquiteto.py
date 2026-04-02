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

# TODO: definir o papel do agente arquiteto
SYSTEM_PROMPT = """
Você é um Arquiteto de Soluções Sênior.

Responsabilidades:
- Traduzir requisios de négocio em arquitetura técnica
- Propor arquitetura em alto nível
- Produzir documentação objetiva e corporativa

Restrições:
- Não detalhar código
- Não assumir ferramentas proprietárias sem solicitação
- Priorizar clareza arquitetural
"""

# ---------------- LLM ----------------
def chamar_llm(prompt):
    resposta = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT}, #Como conteúdo
            {"role": "user", "content": prompt} #Explicando ou pedindo a necesidade de negócio
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
# Implementar tool do agente
def gerar_topicos_arquitetura(projeto):
    return chamar_llm(f"""
    Gere os principais tópicos de uma arquitetura de solução para o seguinte projeto: 
    {projeto}                  

    Responda em lista objetiva.              
    """)

# ---------------- Agente ----------------
# Implementar lógica do agente - Toda a orquestação
def agente_arquiteto(projeto):
    memoria = carregar_memoria()

    if projeto in memoria:
        print("Arquitetura recuperada da memória")
        return memoria[projeto]
    
    print("Analisando o projeto... ")
    topicos = gerar_topicos_arquitetura(projeto=projeto) #Tool

    arquitetura = {
        "projeto": projeto,
        "criacao": datetime.now().isoformat(),
        "arquitetura_sugerida": topicos
    }

    exportar_markdown(arquitetura=arquitetura)
    memoria[projeto] = arquitetura

    salvar_memoria(memoria=memoria)

    return arquitetura


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
