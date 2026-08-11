from PyPDF2 import PdfReader
from docx import Document


def extract_pdf_text(file):
    """
    Extract text from a PDF resume.
    """

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file):
    """
    Extract text from a DOCX resume.
    """

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text


def extract_resume_text(file, filename: str = None):
    """
    Detect file type and extract resume text.

    filename: optional explicit filename (needed when 'file' object
    doesn't have a .name attribute, e.g. FastAPI's UploadFile.file)
    """

    name = filename if filename else getattr(file, "name", "")
    name = name.lower()

    if name.endswith(".pdf"):
        return extract_pdf_text(file)

    elif name.endswith(".docx"):
        return extract_docx_text(file)

    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")