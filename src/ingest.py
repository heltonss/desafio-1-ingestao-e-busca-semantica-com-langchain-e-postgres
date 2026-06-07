import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
for k in ["PDF_PATH", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]:
    if not os.getenv(k):
        raise ValueError(f"{k} variável de ambiente não foi definida")


PDF_PATH = os.getenv("PDF_PATH")

if not PDF_PATH:
    raise ValueError("PDF_PATH não foi definido")

def ingest_pdf():
    docs = PyPDFLoader(PDF_PATH).load()

    TEXT_SPLITS = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150).split_documents(docs)

    if not TEXT_SPLITS:
        raise ValueError("Não foi possível dividir o texto em chunks")

    content = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items()
                      if v not in (None, "")},
        )
        for d in TEXT_SPLITS
    ]

    content_ids = [f"doc-{i}" for i in range(len(content))]
    embeddings = OpenAIEmbeddings(model=os.getenv(
        "OPENAI_MODEL"))

    store = PGVector(
        embeddings=embeddings,
        connection=os.getenv("PGVECTOR_URL"),
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        use_jsonb=True,
    )

    try:
        store.add_documents(documents=content, ids=content_ids)
    except Exception as e:
        print(f"Erro ao adicionar documentos: {e}")
    else:
        print(f"{len(content)} documentos foram ingeridos com sucesso!")


if __name__ == "__main__":
    ingest_pdf()
