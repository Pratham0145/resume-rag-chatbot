import os

from dotenv import load_dotenv

from pinecone import Pinecone


load_dotenv(override=True)


pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)


index_name = "resume-rag"

index = pc.Index(index_name)