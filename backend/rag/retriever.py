# from langchain_huggingface import HuggingFaceEmbeddings

# from langchain_chroma import Chroma


# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# def get_retriever(file_name):

#     db_path = f"chroma_db/{file_name}"

#     vectorstore = Chroma(
#         persist_directory=db_path,
#         embedding_function=embedding_model
#     )

#     retriever = vectorstore.as_retriever(
#         search_kwargs={"k": 3}
#     )

#     return retriever




from langchain_huggingface import HuggingFaceEmbeddings

from langchain_pinecone import PineconeVectorStore


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_retriever(file_name):

    vectorstore = PineconeVectorStore(
        index_name="resume-rag",
        embedding=embedding_model
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {
                "file_name": file_name
            }
        }
    )

    return retriever