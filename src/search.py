import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(question=None):
    if not question:
        raise ValueError("Preciso de uma pergunta para realizar a busca")

    for k in ["PDF_PATH", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]:
        if not os.getenv(k):
            raise ValueError(f"{k} variável de ambiente não foi definida")

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    store = PGVector(
        embeddings=embeddings,
        connection=os.getenv("PGVECTOR_URL"),
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        use_jsonb=True,
    )

    results = store.similarity_search_with_score(query=question, k=10)

    contexto = "\n\n".join(doc.page_content
                           for doc, score in results)

    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"), temperature=0.5)

    # Criar PromptTemplate corretamente
    prompt = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )

    # Chain correto
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "contexto": contexto,
        "pergunta": question
    })
