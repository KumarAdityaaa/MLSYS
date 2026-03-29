from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from utils.pdf_loader import load_pdf
from memory.vector_store import get_vector_store
from langchain.text_splitter import RecursiveCharacterTextSplitter

router = APIRouter()

PDF_DIR = "uploaded_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save file to disk
    file_path = os.path.join(PDF_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        # Load and split PDF into chunks
        docs = load_pdf(file_path)

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # Ingest into ChromaDB vector store
        db = get_vector_store()
        db.add_documents(chunks)

        return {
            "message": f"Successfully indexed {len(chunks)} chunks from {file.filename}",
            "chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
