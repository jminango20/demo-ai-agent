from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama

CHROMA_PATH = "chroma"

def ask_rag(question: str):
    embeddings = OllamaEmbeddings(
        model = "nomic-embed-text"
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    docs = db.similarity_search(query=question, k=4) #Os 4 mais parecidos

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
            Use apenas o contexto abaixo para responder a pergunta.
            Se a resposta não estiver no contexto, diga que não encontrou a informação.

            Contexto:
            {context}

            Pergunta:
            {question}
        """
    
    llm = Ollama(model="mistral")

    return llm.invoke(prompt)
