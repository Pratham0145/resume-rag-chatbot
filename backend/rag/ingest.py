from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_pinecone import PineconeVectorStore

from rag.pinecone_client import index


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def ingest_pdf(file_path, file_name):

    # Load PDF
    loader = PyPDFLoader(file_path)

    documents = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    texts = text_splitter.split_documents(documents)

    # Add metadata
    for text in texts:

        text.metadata["file_name"] = file_name

    # Store in Pinecone
    PineconeVectorStore.from_documents(
        documents=texts,
        embedding=embedding_model,
        index_name="resume-rag"
    )