from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from routes.upload import router as upload_router

from routes.chat import router as chat_router


app = FastAPI(
    title="Resume RAG Chatbot"
)


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==============================
# ROUTES
# ==============================

app.include_router(upload_router)

app.include_router(chat_router)


@app.get("/")
def home():

    return {
        "message": "Resume RAG API Running"
    }