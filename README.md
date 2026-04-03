# Agente Arquiteto de IA (LLM Local com Ollama)

Agente simples que recebe um cenário de negócio, propõe uma arquitetura técnica em alto nível, gera um documento Markdown e reutiliza memória local para projetos já processados.

---

## Estrutura do projeto

```
demo-ai-agent/
├── agente_arquiteto.py     # Agente completo (LLM, memória, tools, orquestração)
├── memoria_agente.json     # Gerado automaticamente (não versionar)
├── requirements.txt
└── .gitignore
```

Arquivos gerados em execução:
- `memoria_agente.json` — memória persistente entre execuções
- `Nome_do_Projeto.md` — documento de arquitetura gerado

---

## Pré-requisitos

- Python 3.10+
- Ollama instalado e rodando

---

## Instalação

```bash
# 1. Criar ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 2. Instalar dependência
pip install openai
```

---

## Modelos no Ollama

```bash
ollama pull mistral
ollama list
```

---

## Como executar

```bash
python agente_arquiteto.py
```

Para testar com outros projetos, edite a lista no final do arquivo:

```python
projetos = [
    "Seu cenário de negócio aqui",
]
```

---

## Fluxo do agente

```
Projeto recebido
      ↓
Existe na memória?
  ├── SIM → retorna da memória (sem chamar LLM)
  └── NÃO → chama tool gerar_topicos_arquitetura()
                  ↓
            LLM (Mistral local)
                  ↓
            Salva .md + memória
                  ↓
            Retorna arquitetura
```

---

## Conceitos do código

| Parte | Função |
|---|---|
| `SYSTEM_PROMPT` | Define o papel do agente (Arquiteto Sênior) |
| `chamar_llm()` | Chama o Mistral via Ollama |
| `carregar_memoria()` / `salvar_memoria()` | Persistência em JSON local |
| `gerar_topicos_arquitetura()` | Tool — gera a arquitetura via LLM |
| `exportar_markdown()` | Tool — salva o resultado em `.md` |
| `agente_arquiteto()` | Orquestra todo o fluxo |

> O LLM não é o agente. O agente decide quando e como usar o LLM.

---

## .gitignore

```gitignore
__pycache__/
*.pyc
.venv/
memoria_agente.json
*.md
!README.md
```