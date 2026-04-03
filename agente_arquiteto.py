import json
from datetime import datetime
from openai import OpenAI
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# ---------------- Configuração LLM ----------------
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "mistral:latest"
MEMORIA_ARQUIVO = "memoria_agente.json"
CHROMA_PATH = "chroma"

SYSTEM_PROMPT = """
Você é um Arquiteto de Soluções Sênior.

Responsabilidades:
- Traduzir requisitos de negócio em arquitetura técnica
- Propor arquitetura em alto nível baseada em padrões reais
- Produzir documentação objetiva e corporativa

Restrições:
- Não detalhar código
- Não assumir ferramentas proprietárias sem solicitação
- Priorizar clareza arquitetural
- Basear-se nos padrões e documentos fornecidos como contexto
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

# ---------------- Tool: RAG ----------------
def buscar_contexto_rag(projeto):
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        docs = db.similarity_search(query=projeto, k=4)

        if not docs:
            print("Nenhum contexto encontrado no RAG.")
            return ""

        print(f"{len(docs)} documentos relevantes encontrados no RAG.")
        return "\n\n".join([doc.page_content for doc in docs])

    except Exception as e:
        print(f"RAG indisponível: {e}")
        return ""

# ---------------- Tool: Gerar Arquitetura ----------------
def gerar_topicos_arquitetura(projeto):
    contexto = buscar_contexto_rag(projeto)

    if contexto:
        prompt = f"""
        Use o contexto abaixo como referência para propor
        uma arquitetura para o projeto.

        Contexto (padrões e referências internas):
        {contexto}

        Projeto:
        {projeto}

        Responda em lista objetiva.
        """
    else:
        prompt = f"""
        Gere os principais tópicos de uma arquitetura de solução
        para o seguinte projeto:

        {projeto}

        Responda em lista objetiva.
        """

    return chamar_llm(prompt)

# ---------------- Tool: Exportar Markdown ----------------
def exportar_markdown(arquitetura):
    nome_arquivo = arquitetura["projeto"].replace(" ", "_") + ".md"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"""# Arquitetura do Projeto

## Projeto
{arquitetura['projeto']}

## Data de Criação
{arquitetura['criacao']}

## Arquitetura Sugerida
{arquitetura['arquitetura_sugerida']}

## Contexto Utilizado
{'RAG (documentos internos)' if arquitetura.get('usou_rag') else 'Conhecimento geral do LLM'}
""")
    return nome_arquivo

# ---------------- Agente ----------------
def agente_arquiteto(projeto):
    memoria = carregar_memoria()

    if projeto in memoria:
        print("Arquitetura recuperada da memória.")
        return memoria[projeto]

    print("Analisando o projeto...")
    topicos = gerar_topicos_arquitetura(projeto)

    arquitetura = {
        "projeto": projeto,
        "criacao": datetime.now().isoformat(),
        "arquitetura_sugerida": topicos,
        "usou_rag": True
    }

    exportar_markdown(arquitetura)
    memoria[projeto] = arquitetura
    salvar_memoria(memoria)

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