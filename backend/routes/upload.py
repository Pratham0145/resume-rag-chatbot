import os

from fastapi import APIRouter, UploadFile, File

from rag.ingest import ingest_pdf


router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:

        f.write(await file.read())

    ingest_pdf(
        file_path,
        file.filename
    )

    return {
        "message": "PDF uploaded successfully",
        "file_name": file.filename
    }