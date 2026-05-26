from fastapi import APIRouter

from fastapi.responses import StreamingResponse

from pydantic import BaseModel

import asyncio

from rag.retriever import get_retriever

from rag.llm import get_llm

from utils.prompt import PROMPT_TEMPLATE

from service.redis_manager import (
    save_message,
    load_messages,
    cache_response,
    get_cached_response
)


router = APIRouter()


class ChatRequest(BaseModel):

    session_id: str

    file_name: str

    query: str


@router.post("/chat")
async def chat(request: ChatRequest):

    # Cache check
    cached_response = get_cached_response(
        request.query
    )

    if cached_response:

        async def cached_stream():

            yield cached_response

        return StreamingResponse(
            cached_stream(),
            media_type="text/plain"
        )


    # Retriever
    retriever = get_retriever(
        request.file_name
    )

    docs = retriever.invoke(
        request.query
    )

    # Context
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # History
    history_messages = load_messages(
        request.session_id
    )

    history = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in history_messages[-5:]
        ]
    )

    # Prompt
    final_prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=f"""
        Previous Conversation:
        {history}

        Current Question:
        {request.query}
        """
    )

    # LLM
    llm = get_llm()


    async def generate_response():

        full_response = ""

        for chunk in llm.stream(final_prompt):

            token = chunk.content

            full_response += token

            yield token

            await asyncio.sleep(0.01)

        # Save memory
        save_message(
            request.session_id,
            "user",
            request.query
        )

        save_message(
            request.session_id,
            "assistant",
            full_response
        )

        # Cache response
        cache_response(
            request.query,
            full_response
        )


    return StreamingResponse(
        generate_response(),
        media_type="text/plain"
    )