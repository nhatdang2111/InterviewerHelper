"""PDF text extraction using PyMuPDF with fallback to image extraction"""
import fitz  # PyMuPDF
import base64
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF. Falls back to empty if image-based.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text content (may be empty for image-based PDFs)
    """
    text_parts = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            if text.strip():
                text_parts.append(text)

    return "\n".join(text_parts)


def is_image_based_pdf(pdf_path: str) -> bool:
    """Check if PDF is image-based (scanned) with no text layer."""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            if page.get_text().strip():
                return False
    return True


def pdf_to_base64_images(pdf_path: str, dpi: int = 150) -> list[str]:
    """Convert PDF pages to base64 encoded PNG images.

    Args:
        pdf_path: Path to PDF file
        dpi: Resolution for rendering (default 150)

    Returns:
        List of base64 encoded PNG images
    """
    images = []
    zoom = dpi / 72  # 72 is default PDF resolution

    with fitz.open(pdf_path) as doc:
        for page in doc:
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            images.append(b64)

    return images


def get_pdf_as_bytes(pdf_path: str) -> bytes:
    """Read PDF file as bytes for API upload."""
    return Path(pdf_path).read_bytes()
