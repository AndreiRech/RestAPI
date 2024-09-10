from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from app.services.csv_service import process_csv

router = APIRouter(prefix="/csv", tags=["CSV"])

CSV_BASE_PATH = Path("app/static/games.csv")

@router.get("/", response_class=FileResponse)
def download_csv_template():
    """
    Rota para baixar o template de CSV base.
    """
    if not CSV_BASE_PATH.exists():
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado.")

    return FileResponse(
        CSV_BASE_PATH, media_type="text/csv", filename="games.csv"
    )
    
@router.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    """
    Rota para receber e processar um arquivo CSV.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um CSV.")

    result = await process_csv(file)
    return {"message": "CSV processado com sucesso", "result": result}
