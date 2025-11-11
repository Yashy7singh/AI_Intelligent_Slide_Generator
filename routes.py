import os
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from src.agents.slide_generator import SlideGenerator
from src.agents.summarizer import Summarizer
from src.agents.content_extractor import ContentExtractor

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """upload a file for slide generation"""
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename, "message": "File uploaded successfully."}

@router.get("/generate/")
async def generate_presentation():
    """generate a presentation from the uploaded file"""
    
    content_extractor = ContentExtractor(directory = UPLOAD_DIR)
    content = content_extractor.extract_content()

   
    summarizer = Summarizer()
    slide_generator = SlideGenerator(output_dir="output/")

    for filename, text in content.items():
        summary = summarizer.summarize(text)
        summary_points = summary.split("\n")
        slide_generator.create_slide(title=filename, content=summary_points)


    pptx_path = "output/generated_presentation.pptx"
    return {"message": "slide generated successfully", "download_url": f"/download/?filename={pptx_path}"}


@router.get("/download/")
async def download_presentation(filename: str):
    """download the generated presentation"""
    return FileResponse(filename, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', filename="AI_Presentation.pptx")