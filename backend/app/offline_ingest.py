"""Offline ingestion script to embed all PDFs under data/raw_pdfs.

Usage (PowerShell):
python -m backend.app.offline_ingest --subject Biology
python -m backend.app.offline_ingest --subject Physics --pattern leph*.pdf

If --subject is omitted, will try to infer subject from filename prefix (leph -> Physics, lebo -> Biology, lemh -> Math) else fallback to 'General'.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Iterable
from .config import settings
from . import pdf_processing
from .embedding_store import add_texts

PDF_DIR = Path('data/raw_pdfs')

PREFIX_SUBJECT = {
    'leph': 'Physics',
    'lebo': 'Biology',
    'lemh': 'Math'
}

def infer_subject(filename: str) -> str:
    lower = filename.lower()
    for prefix, subj in PREFIX_SUBJECT.items():
        if lower.startswith(prefix):
            return subj
    return 'General'

def iter_pdfs(pattern: str | None) -> Iterable[Path]:
    if not PDF_DIR.exists():
        return []
    if pattern:
        return sorted(PDF_DIR.glob(pattern))
    return sorted(PDF_DIR.glob('*.pdf'))

def process_file(path: Path, subject: str, chunk_size: int, overlap: int):
    chunks, meta = pdf_processing.extract_chunks_with_metadata(path, subject, chunk_size, overlap)
    add_texts(chunks, meta)
    return len(chunks)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', help='Override subject for all PDFs')
    parser.add_argument('--pattern', help='Glob pattern to filter PDFs (e.g., leph*.pdf)')
    args = parser.parse_args()

    pdfs = list(iter_pdfs(args.pattern))
    if not pdfs:
        print('No PDFs found.')
        return

    total_chunks = 0
    for pdf in pdfs:
        subj = args.subject or infer_subject(pdf.name)
        count = process_file(pdf, subj, settings.chunk_size, settings.chunk_overlap)
        total_chunks += count
        print(f'Ingested {pdf.name} as {subj}: {count} chunks')
    print(f'Total chunks added: {total_chunks}')

if __name__ == '__main__':
    main()
