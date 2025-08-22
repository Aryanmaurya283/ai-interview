import io
import docx
import pdfplumber
from fastapi import UploadFile
from loguru import logger

def parse_resume(file: UploadFile) -> str:
    """
    Parses the uploaded resume file (PDF or DOCX) and extracts text.

    Args:
        file: The uploaded file from FastAPI.

    Returns:
        The extracted text from the resume as a string.
    """
    file_extension = file.filename.split('.')[-1].lower()
    file_content = file.file.read()

    text = ""
    try:
        if file_extension == 'pdf':
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        elif file_extension == 'docx':
            doc = docx.Document(io.BytesIO(file_content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            logger.warning(f"Unsupported file type: {file_extension}")
            return "Unsupported file type. Please upload a PDF or DOCX file."

        logger.info(f"Successfully parsed resume: {file.filename}")
        return text
    except Exception as e:
        logger.error(f"Error parsing resume {file.filename}: {e}")
        return f"Error parsing file: {e}"
