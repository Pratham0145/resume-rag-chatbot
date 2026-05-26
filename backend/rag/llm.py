import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq


load_dotenv(override=True)


def get_llm():

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0,
        streaming=True
    )

    return llm