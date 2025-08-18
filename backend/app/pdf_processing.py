from pathlib import Path
import fitz  # PyMuPDF
from typing import List, Tuple, Dict


def extract_pages(pdf_path: Path) -> List[Tuple[int, str]]:
    """Return list of (page_number, text). Page numbers are 1-based."""
    doc = fitz.open(pdf_path)
    pages: List[Tuple[int, str]] = []
    for idx, page in enumerate(doc, start=1):
        pages.append((idx, page.get_text()))
    return pages


def chunk_page_text(page_text: str, chunk_size: int, overlap: int) -> List[str]:
    chunks: List[str] = []
    start = 0
    length = len(page_text)
    while start < length:
        end = min(start + chunk_size, length)
        chunk = page_text[start:end]
        chunks.append(chunk)
        if end == length:
            break
        start = end - overlap
    return chunks


def extract_chunks_with_metadata(pdf_path: Path, subject: str, chunk_size: int, overlap: int) -> Tuple[List[str], List[Dict]]:
    """Process a PDF into text chunks and metadata including page numbers."""
    pages = extract_pages(pdf_path)
    all_chunks: List[str] = []
    metadata: List[Dict] = []
    for page_no, text in pages:
        page_chunks = chunk_page_text(text, chunk_size, overlap)
        for chunk in page_chunks:
            all_chunks.append(chunk)
            metadata.append({
                "subject": subject,
                "source": pdf_path.name,
                "page": page_no
            })
    return all_chunks, metadata

