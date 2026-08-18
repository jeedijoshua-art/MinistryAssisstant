from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os

router = APIRouter(prefix="/files", tags=["File Management"])

# Ensure uploads directory exists
UPLOAD_DIR = "/tmp/ztp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "bin"
    file_id = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_id)
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
            
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size_bytes": len(content),
            "url": f"/files/{file_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
