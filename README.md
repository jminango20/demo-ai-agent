# Agente Arquiteto com RAG (LLM Local + Documentos Internos)

Integração entre o Agente Arquiteto e o sistema RAG.
O agente propõe arquiteturas técnicas baseadas nos **documentos internos da empresa**,
não apenas no conhecimento genérico do LLM.

---

## Por que unir Agente + RAG?

| Sem RAG | Com RAG |
|---|---|
| LLM sugere tecnologias genéricas | LLM usa os padrões da sua empresa |
| Pode recomendar ferramentas não aprovadas | Respeita políticas e stack definidos |
| Arquitetura baseada em conhecimento geral | Arquitetura baseada nos seus documentos reais |

> O LLM é o arquiteto. Os documentos são o regulamento interno que ele deve seguir.

---

## Estrutura do projeto

```
demo-ai-agent/
├── app/
│   ├── ingest.py           # Lê docs, gera embeddings, salva no Chroma
│   ├── rag.py              # Busca semântica no Chroma
│   └── main.py             # API REST (FastAPI)
├── data/
│   └── docs/               # Seus documentos internos (PDFs, TXTs)
│       ├── arquitetura.pdf
│       ├── politica-seguranca.txt
│       └── faq.txt
├── chroma/                 # Banco vetorial (gerado automaticamente)
├── agente_arquiteto.py     # Agente integrado com RAG
├── requirements.txt
└── .gitignore
```

---

## Fluxo completo

```
Cenário de negócio recebido
            ↓
  Existe na memória local?
    ├── SIM → retorna sem chamar LLM
    └── NÃO ↓
            ↓
  Tool: buscar_contexto_rag()
            ↓
  nomic-embed-text vetoriza a pergunta
            ↓
  Chroma busca os 4 docs mais similares
            ↓
  Encontrou contexto?
    ├── NÃO → usa apenas conhecimento geral do LLM
    └── SIM ↓
            ↓
  Monta prompt:
    "Use este contexto (docs internos) +
     este cenário de negócio →
     proponha uma arquitetura"
            ↓
  Mistral (LLM local) raciocina e estrutura
            ↓
  Gera arquitetura baseada nos seus documentos
            ↓
  Exporta .md + salva memória JSON
```

---

## O que cada parte faz

| Parte | Responsabilidade |
|---|---|
| `nomic-embed-text` | Converte texto em vetores numéricos |
| `Chroma` | Armazena e busca vetores por similaridade semântica |
| `buscar_contexto_rag()` | Tool que recupera docs relevantes para o projeto |
| `gerar_topicos_arquitetura()` | Tool que chama o LLM com contexto real |
| `Mistral` | Raciocina, estrutura e redige a arquitetura |
| `agente_arquiteto()` | Orquestra todo o fluxo |

> O LLM não acessa o Chroma diretamente.
> O agente busca o contexto e monta o prompt antes de chamar o LLM.

---

## Pré-requisitos

- Python 3.10+
- Ollama instalado e rodando

---

## Instalação

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Modelos no Ollama

```bash
ollama pull mistral
ollama pull nomic-embed-text
ollama list
```

---

## Como executar

### 1. Adicionar documentos internos

Coloque seus PDFs e TXTs em `data/docs/`:

```
data/docs/
├── padroes-arquiteturais.pdf   # padrões da empresa
├── politica-seguranca.txt      # tecnologias aprovadas
└── stack-tecnologico.pdf       # infra e ferramentas
```

### 2. Ingestão (gera embeddings e salva no Chroma)

```bash
python app/ingest.py
# Output: Ingestão concluída: X chunks criados.
```

> Execute sempre que adicionar novos documentos.

### 3. Executar o agente

```bash
python agente_arquiteto.py
```

Para testar com outros cenários, edite a lista no final do arquivo:

```python
projetos = [
    "Seu cenário de negócio aqui",
]
```

---

## Exemplo de resultado

**Entrada:**
```
"Criar painel de BI para acompanhamento de vendas"
```

**Sem RAG** — LLM sugere livremente:
```
- Autenticação com AWS Cognito
- Deploy na AWS
- MongoDB para armazenamento
```

**Com RAG** — LLM usa seus documentos:
```
- Autenticação com Keycloak (conforme politica-seguranca.txt)
- Deploy na Oracle Cloud (conforme stack-tecnologico.pdf)
- PostgreSQL como banco de dados (padrão interno)
```