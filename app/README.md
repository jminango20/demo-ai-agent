# Agente RAG Local com Ollama

Projeto didático para construir um agente de **Recuperação de Informação com Geração (RAG)** usando LLM local via Ollama, sem custo de API e sem enviar dados para nuvem.

---

## O que este projeto faz

- Lê documentos PDF e TXT de uma pasta local em /data/docs
- Divide os documentos em chunks e gera embeddings
- Armazena os vetores em um banco vetorial (Chroma)
- Expõe uma API REST para perguntas em linguagem natural
- Responde usando **apenas o conteúdo dos documentos** como contexto

---

## Conceitos demonstrados

| Conceito | O que é |
|---|---|
| **LLM** | Mistral rodando localmente via Ollama |
| **Embedding** | Modelo que converte texto em vetores numéricos |
| **Chroma** | Banco de dados vetorial local |
| **RAG** | Busca contexto relevante antes de chamar o LLM |
| **FastAPI** | API REST que expõe o agente |

---

## Estrutura do projeto

```
demo-ai-agent/
├── app/
│   ├── ingest.py       # Lê docs, gera embeddings, salva no Chroma
│   ├── rag.py          # Busca no Chroma e chama o LLM
│   └── main.py         # API REST com FastAPI
├── data/
│   └── docs/           # Coloque aqui seus PDFs e TXTs
├── chroma/             # Gerado automaticamente (não versionar)
├── requirements.txt
└── .gitignore
```

---

## Pré-requisitos

- Python **3.10+**
- Ollama instalado e rodando
- Git Bash ou PowerShell

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/jminango20/demo-ai-agent
cd demo-ai-agent
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Baixar os modelos no Ollama

```bash
# Modelo de chat (geração de texto)
ollama pull mistral

# Modelo de embeddings (vetorização)
ollama pull nomic-embed-text

# Verificar
ollama list
```

---

## Como executar

### Passo 1 — Adicionar documentos

Coloque seus arquivos `.pdf` ou `.txt` na pasta `data/docs/`.

### Passo 2 — Ingestão (gera embeddings e salva no Chroma)

```bash
python app/ingest.py
# Output: Ingestão concluída: X chunks criados.
```

> ⚠️ Execute este passo sempre que adicionar novos documentos.

### Passo 3 — Subir a API

```bash
uvicorn app.main:app --reload
```

### Passo 4 — Fazer uma pergunta

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/pergunta" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question": "Sua pergunta aqui"}'
```

**Git Bash:**
```bash
curl -X POST http://localhost:8000/pergunta \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Sua pergunta aqui\"}"
```

---

## Fluxo interno

```
Pergunta do usuário
       ↓
  Gera embedding da pergunta (nomic-embed-text)
       ↓
  Busca os 4 chunks mais similares no Chroma
       ↓
  Monta prompt com o contexto encontrado
       ↓
  Chama o Mistral com o prompt
       ↓
  Retorna resposta baseada apenas nos documentos
```

---

## requirements.txt

```
langchain
langchain-community
langchain-ollama
langchain-chroma
langchain-text-splitters
pypdf
fastapi
uvicorn
```

---

## .gitignore

```gitignore
# Banco vetorial (gerado automaticamente)
chroma/

# Documentos locais
data/docs/

# Ambiente virtual
.venv/

# Python cache
__pycache__/
*.pyc

# Variáveis de ambiente
.env
```

---

## Diferença entre os dois modelos usados

| Modelo | Função | Quando é chamado |
|---|---|---|
| `nomic-embed-text` | Converte texto em vetores | Na ingestão e na pergunta |
| `mistral` | Gera a resposta em linguagem natural | Apenas na pergunta |

O `nomic-embed-text` **não gera texto**, apenas vetoriza. O `mistral` **não acessa o Chroma**, apenas recebe o contexto já montado.
