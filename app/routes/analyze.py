from fastapi import APIRouter, UploadFile, File
from app.services.file_service import process_uploaded_zip

router = APIRouter()

@router.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
    result = await process_uploaded_zip(file)
    return result