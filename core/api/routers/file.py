from fastapi import APIRouter, UploadFile
from openpyxl import load_workbook
import io

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.post("/upload")
async def upload_file(file: UploadFile):
    contents = file.file.read()
    filename=io.BytesIO(contents)
    book = load_workbook(filename=filename)
    sheet = book.active
    print(sheet['A2'])
    return file